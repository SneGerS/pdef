# encoding: utf-8
import logging
import os.path
from jinja2 import Environment
from pdef.common import Type, upper_first, mkdir_p


class JavaTranslator(object):
    def __init__(self, out):
        self.out = out

        self.env = Environment(trim_blocks=True)
        self.enum_template = self.read_template('enum.template')
        self.message_template = self.read_template('message.template')
        self.interface_template = self.read_template('interface.template')

    def write_definition(self, def0):
        '''Writes a java definition to the output directory.'''
        jdef = self.definition(def0)
        code = jdef.code

        dirs = jdef.package.split('.')
        fulldir = os.path.join(self.out, os.path.join(*dirs))
        fullpath = os.path.join(fulldir, jdef.name, '.java')

        mkdir_p(fulldir)
        with open(fullpath, 'wt') as f:
            f.write(code)

        logging.info('%s: created %s', self, fullpath)

    def definition(self, def0):
        '''Creates and returns a java definition.'''
        t = def0.type
        if t == Type.ENUM: JavaEnum(def0, self.enum_template)
        elif t == Type.MESSAGE: JavaMessage(def0, self.message_template)
        elif t == Type.INTERFACE: JavaInterface(def0, self.interface_template)
        raise ValueError('Unsupported definition %s' % def0)

    def read_template(self, name):
        path = os.path.join(os.path.dirname(__file__), name)
        with open(path, 'r') as f:
            text = f.read()
        return self.env.from_string(text)


class JavaDefinition(object):
    def __init__(self, obj, template):
        self.name = obj.name
        self.package = obj.module.name
        self._template = template

    @property
    def code(self):
        return self._template.render(**self.__dict__)


class JavaEnum(JavaDefinition):
    def __init__(self, enum, template):
        super(JavaEnum, self).__init__(enum, template)
        self.values = [val.name for val in enum.values.values()]


class JavaMessage(JavaDefinition):
    def __init__(self, msg, template):
        super(JavaMessage, self).__init__(msg, template)

        self.base = ref(msg.base) if msg.base else 'io.pdef.GeneratedMessage'
        self.base_type = ref(msg.base_type) if msg.base_type else None
        self.base_builder = '%s.Builder' % self.base
        self.discriminator_field = JavaField(msg.discriminator_field) \
            if msg.discriminator_field else None
        self.subtypes = tuple((key.name.lower(), ref(val)) for key, val in msg.subtypes.items())

        self.fields = [JavaField(f) for f in msg.fields.values()]
        self.declared_fields = [JavaField(f) for f in msg.declared_fields.values()]
        self.inherited_fields = [JavaField(f) for f in msg.inherited_fields.values()]
        self.is_exception = msg.is_exception


class JavaField(object):
    def __init__(self, field):
        self.name = field.name
        self.type = ref(field.type)

        self.get = 'get%s' % upper_first(self.name)
        self.set = 'set%s' % upper_first(self.name)
        self.clear = 'clear%s' % upper_first(self.name)
        self.present = 'has%s' % upper_first(self.name)


class JavaInterface(JavaDefinition):
    def __init__(self, iface, template):
        super(JavaInterface, self).__init__(iface, template)

        self.bases = [ref(base) for base in iface.bases]
        self.declared_methods = [JavaMethod(method) for method in iface.declared_methods.values()]


class JavaMethod(object):
    def __init__(self, method):
        self.name = method.name
        self.args = list((arg.name, ref(arg.type)) for arg in method.args.values())
        self.result = ref(method.result)
        if not self.result.is_interface:
            self.result = 'ListenableFuture<%s>' % self.result.boxed


def ref(obj):
    t = obj.type
    if t in NATIVE_MAP: return NATIVE_MAP[t]

    elif t == Type.LIST: return JavaType(Type.LIST,
            name='java.lang.List<%s>' % ref(obj.element),
            default='com.google.common.collect.ImmutableList.of()')

    elif t == Type.SET: return JavaType(Type.SET,
            name='java.lang.Set<%s>' % ref(obj.element),
            default='com.google.common.collect.ImmutableSet.of()')

    elif t == Type.MAP: return JavaType(Type.MAP,
            name='java.lang.Map<%s, %s>' % (ref(obj.key), ref(obj.val)),
            default='com.google.common.collect.ImmutableMap.of()')

    elif t == Type.ENUM_VALUE: return JavaType(Type.ENUM_VALUE,
            name='%s.%s' % (obj.enum, obj.name))

    name = '%s.%s' % (obj.module.name, obj.name) if obj.module else obj.name
    default = '%s.getInstance()' % name if t == Type.MESSAGE else 'null'
    return JavaType(t, name, default=default)


class JavaType(object):
    def __init__(self, type, name, boxed=None, default='null', is_primitive=False):
        self.type = type
        self.name = name
        self.boxed = boxed if boxed else self
        self.default = default

        self.is_primitive = is_primitive
        self.is_nullable = True
        self.is_nullable = default == 'null'

        self.is_interface = type == Type.INTERFACE
        self.is_list = type == Type.LIST
        self.is_set = type == Type.SET
        self.is_map = type == Type.MAP

    def __str__(self):
        return self.name


NATIVE_MAP = {
    Type.BOOL: JavaType(Type.BOOL, 'boolean', 'Boolean', default='false', is_primitive=True),
    Type.INT16: JavaType(Type.INT16, 'short', 'Short', default='(short) 0', is_primitive=True),
    Type.INT32: JavaType(Type.INT32, 'int', 'Integer', default='0', is_primitive=True),
    Type.INT64: JavaType(Type.INT64, 'long', 'Long', default='0L', is_primitive=True),
    Type.FLOAT: JavaType(Type.FLOAT, 'float', 'Float', default='0f', is_primitive=True),
    Type.DOUBLE: JavaType(Type.DOUBLE, 'double', 'Double', default='0.0', is_primitive=True),
    Type.STRING: JavaType(Type.STRING, 'String'),
    Type.OBJECT: JavaType(Type.OBJECT, 'Object'),
    Type.VOID: JavaType(Type.VOID, 'void', 'Void', is_primitive=True)
}