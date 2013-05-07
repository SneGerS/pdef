# encoding: utf-8
import unittest
from pdef import ast
from pdef.consts import Type
from pdef.lang2 import *


class TestModule(unittest.TestCase):
    def test_lookup_value(self):
        '''Should lookup a value by its ref.'''
        module = Module('test')
        int64 = module.lookup(ast.Ref(Type.INT64))
        assert int64 is Values.INT64

    def test_lookup_list(self):
        '''Should create and link a list by its ref.'''
        module = Module('test')
        list0 = module.lookup(ast.ListRef(ast.Ref(Type.STRING)))
        assert isinstance(list0, List)
        assert list0.element is Values.STRING

    def test_lookup_set(self):
        '''Should create and link a set by its ref.'''
        module = Module('test')
        set0 = module.lookup(ast.SetRef(ast.Ref(Type.FLOAT)))
        assert isinstance(set0, Set)
        assert set0.element is Values.FLOAT

    def test_lookup_map(self):
        '''Should create and link a map by its ref.'''
        module = Module('test')
        map0 = module.lookup(ast.MapRef(ast.Ref(Type.STRING), ast.Ref(Type.INT32)))
        assert isinstance(map0, Map)
        assert map0.key is Values.STRING
        assert map0.value is Values.INT32

    def test_lookup_enum_value(self):
        '''Should look up an enum value.'''
        enum = Enum('Number')
        enum.add_value('ONE')

        module = Module('test')
        module.add_definition(enum)
        one = module.lookup(ast.EnumValueRef(ast.DefinitionRef('Number'), 'ONE'))
        assert one is enum.values['ONE']

    def test_lookup_enum_value_not_present(self):
        '''Should raise an error when an enum does not have a specified value.'''
        enum = Enum('Number')
        module = Module('test')
        module.add_definition(enum)

        try:
            module.lookup(ast.EnumValueRef(ast.DefinitionRef('Number'), 'ONE'))
            self.fail()
        except Exception, e:
            assert 'not found' in e.message

    def test_lookup_user_defined(self):
        '''Should look up a user-defined definition by its reference.'''
        def0 = Definition(Type.DEFINITION, 'Test')

        module = Module('test')
        module.add_definition(def0)

        ref = ast.DefinitionRef('Test')
        result = module.lookup(ref)
        assert def0 is result

    def test_lookup_link(self):
        '''Should look up a definition by its reference and link the definition.'''
        def0 = Definition(Type.DEFINITION, 'Test')

        module = Module('test')
        module.add_definition(def0)

        ref = ast.DefinitionRef('Test')
        result = module.lookup(ref)
        assert result._linked


class TestEnum(unittest.TestCase):
    def test_from_ast(self):
        '''Should create an enum from an AST node.'''
        node = ast.Enum('Number', values=('ONE', 'TWO', 'THREE'))
        enum = Enum.from_ast(node)

        assert len(enum.values) == 3
        assert 'ONE' in enum.values
        assert 'TWO' in enum.values
        assert 'THREE' in enum.values

    def test_add_value(self):
        '''Should add to enum a new value by its name.'''
        enum = Enum('Number')
        one = enum.add_value('ONE')

        assert isinstance(one, EnumValue)
        assert one.name == 'ONE'
        assert one.enum is enum


class TestMessage(unittest.TestCase):
    def test_from_ast(self):
        '''Should create a message from an AST node.'''
        node = ast.Message('Msg', base=ast.DefinitionRef('Base'),
                           fields=[ast.Field('field', ast.Ref(Type.INT32))])
        msg = Message.from_ast(node)
        assert msg.name == node.name
        assert msg._node == node

    def test_link(self):
        '''Should init and link a message when its AST node present.'''
        base = Message('Base')
        module = Module('test')
        module.add_definition(base)

        node = ast.Message('Msg', base=ast.DefinitionRef('Base'),
                           fields=[ast.Field('field', ast.Ref(Type.INT32))])
        msg = Message.from_ast(node, module)
        msg.link()

        assert msg.base is base
        assert msg.base_type is None
        field = msg.declared_fields['field']
        assert field.name == 'field'
        assert field.type is Values.INT32

    def test_set_base(self):
        '''Should set a message base.'''
        base = Message('Base')
        msg = Message('Msg')
        msg.set_base(base)

        assert base in msg._bases

    def test_set_base_self_inheritance(self):
        '''Should prevent self-inheritance.'''
        msg = Message('Msg')
        try:
            msg.set_base(msg)
            self.fail()
        except Exception, e:
            assert 'cannot inherit itself' in e.message

    def test_set_base_circular_inheritance(self):
        '''Should prevent circular inheritance.'''
        msg0 = Message('Msg0')
        msg1 = Message('Msg1')

        msg0.set_base(msg1)
        try:
            msg1.set_base(msg0)
            self.fail()
        except Exception, e:
            assert 'circular inheritance' in e.message

    def test_set_base_message_exception_clash(self):
        '''Should prevent message<->exception inheritance.'''
        msg = Message('Msg')
        exc = Message('Exc', is_exception=True)

        try:
            exc.set_base(msg)
            self.fail()
        except Exception, e:
            assert 'cannot inherit' in e.message

    def test_set_base_add_subtypes(self):
        '''Should set a message base with a base type and add the message to the base subtypes.'''
        enum = Enum('Type')
        subtype = enum.add_value('SUBTYPE')

        base = Message('Base')
        base.add_field('type', enum, is_discriminator=True)
        msg = Message('Msg')
        msg.set_base(base, subtype)

        assert msg.base is base
        assert msg.base_type is subtype
        assert subtype in base.subtypes
        assert base.subtypes[subtype] is msg

    def test_set_base_subtype_tree(self):
        '''Should set a message base with a base type and add the message to the subtype tree.'''
        enum = Enum('Type')
        type0 = enum.add_value('Type0')
        type1 = enum.add_value('Type1')

        base = Message('Base')
        base.add_field('type', enum, is_discriminator=True)

        msg0 = Message('Msg0')
        msg0.set_base(base, type0)

        msg1 = Message('Msg1')
        msg1.set_base(msg0, type1)

        assert msg0.subtypes == {type1 : msg1}
        assert base.subtypes == {type0: msg0, type1: msg1}

    def test_add_field(self):
        msg = Message('Msg')
        msg.add_field('field', Values.INT32)

        field = msg.declared_fields['field']
        assert field.name == 'field'
        assert field.type == Values.INT32

    def test_add_field_duplicate(self):
        msg = Message('Msg')
        msg.add_field('field', Values.INT32)
        try:
            msg.add_field('field', Values.INT32)
        except Exception, e:
            assert 'duplicate' in e.message

    def test_add_field_set_discriminator(self):
        enum = Enum('Type')
        msg = Message('Msg')

        field = msg.add_field('type', enum, is_discriminator=True)
        assert field.is_discriminator
        assert msg.discriminator_field is field


class TestInterface(unittest.TestCase):
    def test_from_ast(self):
        '''Should create an interface from an AST node.'''
        node = ast.Interface('Iface', bases=[ast.DefinitionRef('Base')],
            methods=[ast.Method('echo', args=[ast.MethodArg('text', ast.Ref(Type.STRING))],
                                result=ast.Ref(Type.STRING))])
        iface = Interface.from_ast(node)
        assert iface.name == node.name
        assert iface._node is node

    def test_link(self):
        '''Should init and link an interface from an AST node if present.'''
        base = Interface('Base')
        module = Module('test')
        module.add_definition(base)

        node = ast.Interface('Iface', bases=[ast.DefinitionRef('Base')],
            methods=[ast.Method('echo', args=[ast.MethodArg('text', ast.Ref(Type.STRING))],
                                result=ast.Ref(Type.STRING))])
        iface = Interface.from_ast(node, module=module)
        iface.link()

        assert iface.bases == [base]

        method = iface.declared_methods['echo']
        assert method.name == 'echo'
        assert method.result is Values.STRING

        arg = method.args['text']
        assert arg.name == 'text'
        assert arg.type is Values.STRING

    def test_add_base(self):
        '''Should add a base to the interface.'''
        base = Interface('Base')
        iface = Interface('Iface')
        iface.add_base(base)
        assert iface.bases == [base]

    def test_add_base_self_inheritance(self):
        '''Should prevent interface self-inheritance.'''
        iface = Interface('Iface')
        try:
            iface.add_base(iface)
            self.fail()
        except Exception, e:
            assert 'self inheritance' in e.message

    def test_add_base_duplicate(self):
        '''Should prevent duplicate interface bases.'''
        base = Interface('Base')
        iface = Interface('Iface')
        iface.add_base(base)
        try:
            iface.add_base(base)
            self.fail()
        except Exception, e:
            assert 'duplicate' in e.message

    def test_add_base_circular_inheritance(self):
        '''Should prevent circular interface inheritance.'''
        iface0 = Interface('Iface0')
        iface1 = Interface('Iface1')
        iface2 = Interface('Iface2')

        iface1.add_base(iface0)
        iface2.add_base(iface1)

        try:
            iface0.add_base(iface2)
            self.fail()
        except Exception, e:
            assert 'circular' in e.message

    def test_add_method(self):
        '''Should add a new method to this interface.'''
        iface = Interface('Calc')
        method = iface.add_method('sum', Values.INT32, ('i0', Values.INT32), ('i1', Values.INT32))

        assert 'sum' in iface.declared_methods
        assert method.name == 'sum'
        assert method.result is Values.INT32

        i0 = method.args['i0']
        i1 = method.args['i1']
        assert i0.name == 'i0'
        assert i1.name == 'i1'
        assert i0.type is Values.INT32
        assert i1.type is Values.INT32

    def test_add_method_duplicate(self):
        '''Should prevent duplicate methods in interfaces.'''
        iface = Interface('Iface')
        iface.add_method('doNothing')
        try:
            iface.add_method('doNothing')
            self.fail()
        except Exception, e:
            assert 'duplicate' in e.message
