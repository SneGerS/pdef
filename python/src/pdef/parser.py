# encoding: utf-8
import logging
import ply.lex as lex
import ply.yacc as yacc

from pdef import ast


class Tokens(object):
    # Simple reserved words.
    reserved = ('AS', 'ENUM', 'EXCEPTION', 'EXTENDS', 'IMPORT', 'INTERFACE', 'INHERITS',
                'MESSAGE', 'ON', 'POLYMORPHIC', 'MODULE', 'NATIVE')

    # All tokens.
    tokens = reserved + (
        'COLON', 'COMMA', 'SEMI',
        'LESS', 'GREATER',
        'LBRACE', 'RBRACE',
        'LBRACKET', 'RBRACKET',
        'LPAREN', 'RPAREN',
        'IDENTIFIER', 'STRING')

    # Regular expressions for simple rules
    t_COLON = r'\:'
    t_COMMA = r'\,'
    t_SEMI = r'\;'
    t_LESS = r'\<'
    t_GREATER = r'\>'
    t_LBRACE  = r'\{'
    t_RBRACE  = r'\}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    # Ignored characters
    t_ignore = " \t"

    # Reserved words map {lowercase: UPPERCASE}.
    # Used as a type in IDENTIFIER.
    reserved_map = {}
    for r in reserved:
        reserved_map[r.lower()] = r

    def t_STRING(self, t):
        r'\".+?\"'
        t.value = t.value.strip('"')
        return t

    def t_IDENTIFIER(self, t):
        r'~?[a-zA-Z_]{1}[a-zA-Z0-9_]*(\.[a-zA-Z_]{1}[a-zA-Z0-9_]*)*'
        t.type = self.reserved_map.get(t.value, "IDENTIFIER")
        if t.value.startswith('~'): # Allows to use reserved words.
            t.value = t.value[1:]

        return t

    def t_comment(self, t):
        r'//.*\n'
        t.lineno += 1

    # Skip the new line and increment the lineno counter.
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    # Print the error message
    def t_error(self, t):
        self._error("Illegal character %s", t.value[0])
        t.lexer.skip(1)

    def _error(self, msg, *args):
        raise NotImplementedError()


class GrammarRules(object):
    # Starting point.
    def p_module(self, t):
        '''
        module : module_name imports definitions
        '''
        name = t[1]
        imports = t[2]
        definitions = t[3]
        t[0] = ast.Module(name, imports=imports, definitions=definitions)

    # Empty token to support optional values.
    def p_empty(self, t):
        '''
        empty :
        '''
        pass

    # The first line is a file.
    def p_module_name(self, t):
        '''
        module_name : MODULE IDENTIFIER SEMI
        '''
        t[0] = t[2]

    # Optional module imports.
    def p_imports(self, t):
        '''
        imports : imports import
                | import
                | empty
        '''
        self._list(t)

    # Package import.
    def p_import(self, t):
        '''
        import : IMPORT IDENTIFIER AS IDENTIFIER SEMI
               | IMPORT IDENTIFIER SEMI
        '''
        name = t[2]
        alias = name if len(t) == 4 else t[4]
        t[0] = ast.ImportRef(name, alias)

    # Type reference with optional generic arguments.
    def p_type(self, t):
        '''
        type : IDENTIFIER LESS types GREATER
             | IDENTIFIER
        '''
        name = t[1]
        vars = [] if len(t) == 2 else t[3]
        t[0] = ast.Ref(name, variables=vars)

    # List of generic arguments.
    def p_types(self, t):
        '''
        types : types COMMA type
              | type
        '''
        self._list(t, separated=1)

    # List of type definitions.
    def p_definitions(self, t):
        '''
        definitions : definitions definition
                    | definition
        '''
        self._list(t)

    # Single type definition.
    def p_definition(self, t):
        '''
        definition : native
                   | enum
                   | message
                   | interface
        '''
        t[0] = t[1]

    # Native type definition.
    def p_native(self, t):
        '''
        native : NATIVE IDENTIFIER variables LBRACE native_options RBRACE
        '''
        name = t[2]
        variables = t[3]
        options = dict(t[5])
        t[0] = ast.Native(name, variables=variables, options=options)

    # Native options: k: v, k1: v2
    def p_native_options(self, t):
        '''
        native_options : native_options COMMA native_option
                       | native_option
                       | empty
        '''
        self._list(t, separated=True)

    # Native option: name: value;
    def p_native_option(self, t):
        '''
        native_option : IDENTIFIER COLON STRING
        '''
        t[0] = (t[1], t[3])

    # Enum definition.
    def p_enum(self, t):
        '''
        enum : ENUM IDENTIFIER LBRACE enum_values RBRACE
        '''
        t[0] = ast.Enum(t[2], values=t[4])

    # List of enum values.
    def p_enum_values(self, t):
        '''
        enum_values : enum_values COMMA enum_value
                    | enum_value
        '''
        self._list(t, separated=1)

    # Single enum value
    def p_enum_value(self, t):
        '''
        enum_value : IDENTIFIER
        '''
        t[0] = t[1]

    # Message definition
    def p_message(self, t):
        '''
        message : message_or_exc IDENTIFIER message_base message_type message_body
        '''
        is_exception = t[1].lower() == 'exception'
        name = t[2] # identifier
        base, subtype = t[3]
        type_field, _type = t[4]
        options, declared_fields = t[5]

        t[0] = ast.Message(name, base=base, subtype=subtype,type_field=type_field,
            type=_type, declared_fields=declared_fields, options=options,
            is_exception=is_exception)

    # Message or exception
    def p_message_or_exception(self, t):
        '''
        message_or_exc : MESSAGE
                       | EXCEPTION
        '''
        t[0] = t[1]

    # Message inheritance
    def p_message_base(self, t):
        '''
        message_base : INHERITS type AS IDENTIFIER
                     | empty
        '''
        if len(t) == 2:
            t[0] = None, None
        else:
            t[0] = t[2], ast.Ref(t[4])

    def p_message_type(self, t):
        '''
        message_type : POLYMORPHIC ON STRING AS IDENTIFIER
                     | empty
        '''
        if len(t) == 2:
            t[0] = None, None
        else:
            tree_field = t[3]
            tree_type = ast.Ref(t[5])
            t[0] = tree_field, tree_type

    def p_message_body(self, t):
        '''
        message_body : LBRACE options fields RBRACE
        '''
        t[0] = t[2], t[3]

    # List of message fields
    def p_fields(self, t):
        '''
        fields : fields field
               | field
               | empty
        '''
        self._list(t)

    # Single message field
    def p_field(self, t):
        '''
        field : IDENTIFIER type SEMI
        '''
        t[0] = ast.Field(t[1], type=t[2])

    # Interface definition
    def p_interface(self, t):
        '''
        interface : INTERFACE IDENTIFIER interface_bases interface_body
        '''
        name = t[2]
        bases = t[3]
        methods = t[4]
        t[0] = ast.Interface(name, bases=bases, methods=methods)

    def p_interface_bases(self, t):
        '''
        interface_bases : EXTENDS types
                        | empty
        '''
        if len(t) == 2:
            t[0] = []
        else:
            t[0] = t[2]

    # Interface methods
    def p_interface_body(self, t):
        '''
        interface_body : LBRACE methods RBRACE
        '''
        t[0] = t[2]

    def p_methods(self, t):
        '''
        methods : methods method
                | method
                | empty
        '''
        self._list(t)

    def p_method(self, t):
        '''
        method : IDENTIFIER LPAREN method_args RPAREN type SEMI
        '''
        name = t[1]
        args = t[3]
        result = t[5]
        t[0] = ast.Method(name, args=args, result=result)

    def p_method_args(self, t):
        '''
        method_args : method_args COMMA method_arg
                    | method_arg
                    | empty
        '''
        self._list(t, separated=1)

    def p_method_arg(self, t):
        '''
        method_arg : IDENTIFIER type
        '''
        t[0] = ast.MethodArg(t[1], t[2])

    # Generic variables in a definition name.
    def p_variables(self, t):
        '''
        variables : LESS variable_list GREATER
                  | empty
        '''
        if len(t) == 2:
            t[0] = []
        else:
            t[0] = t[2]

    # List of variable names in variables.
    def p_variable_list(self, t):
        '''
        variable_list : variable_list COMMA variable
                      | variable
        '''
        self._list(t, separated=1)

    # Generic variable in a definition name.
    def p_variable(self, t):
        '''
        variable : IDENTIFIER
        '''
        t[0] = t[1]

    # Definition and field options.
    def p_options(self, t):
        '''
        options : LBRACKET option_list RBRACKET
                | empty
        '''
        if len(t) == 2:
            t[0] = []
        else:
            t[0] = t[2]

    def p_option_list(self, t):
        '''
        option_list : option_list COMMA option
                    | option
        '''
        self._list(t, separated=1)

    def p_option(self, t):
        '''
        option : IDENTIFIER
        '''
        t[0] = t[1]

    def p_error(self, t):
        self._error("Syntax error at '%s', line %s", t.value, t.lexer.lineno)

    def _list(self, t, separated=False):
        '''List builder, supports separated and empty lists.

        Supported grammar:
        list : list [optional separator] item
             | item
             | empty
        '''
        if len(t) == 1:
            t[0] = []
        elif len(t) == 2:
            if t[1] is None:
                t[0] = []
            else:
                t[0] = [t[1]]
        else:
            t[0] = t[1]
            if not separated:
                t[0].append(t[2])
            else:
                t[0].append(t[3])

    def _error(self, msg, *args):
        raise NotImplementedError()


class ModuleParser(Tokens, GrammarRules):
    def __init__(self, debug=False):
        super(ModuleParser, self).__init__()
        self.debug = debug
        self.lexer = lex.lex(module=self, debug=debug)
        self.parser = yacc.yacc(module=self, debug=debug, tabmodule='pdef.parsetab')
        self.errors = []

    def parse(self, s, **kwargs):
        return self.parser.parse(s, debug=self.debug, **kwargs)

    def _error(self, msg, *args):
        logging.error(msg, *args)
        self.errors.append(msg % args)
