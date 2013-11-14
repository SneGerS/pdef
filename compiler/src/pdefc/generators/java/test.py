# encoding: utf-8
import unittest
from pdefc.ast import *
from pdefc.generators.java import *


class TestJavaEnum(unittest.TestCase):
    def _fixture(self):
        enum = Enum('Number', value_names=['ONE', 'TWO'])
        module = Module('test.module')
        module.add_definition(enum)
        module.link()

        return JavaEnum(enum, jreference)

    def test_constructor(self):
        jenum = self._fixture()
        assert jenum.name == 'Number'
        assert jenum.values == ['ONE', 'TWO']

    def test_render(self):
        jenum = self._fixture()
        templates = jtemplates()
        assert jenum.render(templates)


class TestMessage(unittest.TestCase):
    def _fixture(self):
        enum = Enum('Type')
        subtype = enum.create_value('SUBTYPE')

        base = Message('Base')
        base.create_field('type', enum, is_discriminator=True)

        msg = Message('Message', base=base, discriminator_value=subtype)
        msg.create_field('field', NativeType.BOOL)

        module = Module('test.module')
        module.add_definition(enum)
        module.add_definition(base)
        module.add_definition(msg)
        module.link()

        return JavaDefinition.create(msg, jreference)

    def test_constructor(self):
        jmsg = self._fixture()
        assert jmsg.name == 'Message'
        assert jmsg.is_exception is False
        assert jmsg.base.name == 'test.module.Base'
        assert jmsg.discriminator_value.name == 'test.module.Type.SUBTYPE'
        assert jmsg.subtypes == ()

        assert len(jmsg.declared_fields) == 1
        assert len(jmsg.inherited_fields) == 1
        assert len(jmsg.fields) == 2

    def test_render(self):
        jmsg = self._fixture()
        templates = jtemplates()
        assert jmsg.render(templates)


class TestInterface(unittest.TestCase):
    def _fixture(self):
        exc = Message('Exception', is_exception=True)

        iface = Interface('Interface', exc=exc)
        iface.create_method('method0', NativeType.INT32, [('arg', NativeType.INT32)])
        iface.create_method('method1', NativeType.STRING, [('name', NativeType.STRING)])

        module = Module('test.module')
        module.add_definition(exc)
        module.add_definition(iface)
        module.link()

        return JavaDefinition.create(iface, jreference)

    def test_constructor(self):
        jiface = self._fixture()
        assert jiface.name == 'Interface'
        assert jiface.exc.name == 'test.module.Exception'
        assert len(jiface.declared_methods) == 2

    def test_render(self):
        jiface = self._fixture()
        templates = jtemplates()
        assert jiface.render(templates)


class TestRef(unittest.TestCase):
    def test_native(self):
        for ntype in NativeType.all():
            ref = jreference(ntype)
            assert ref is NATIVE_TYPES[ntype.type]

    def test_list(self):
        list0 = List(NativeType.INT32)
        ref = jreference(list0)

        assert ref.name == 'java.util.List<Integer>'
        assert ref.default == 'new java.util.ArrayList<Integer>()'
        assert ref.descriptor == 'io.pdef.descriptors.Descriptors.list(io.pdef.descriptors.Descriptors.int32)'

    def test_set(self):
        set0 = Set(NativeType.BOOL)
        ref = jreference(set0)

        assert ref.name == 'java.util.Set<Boolean>'
        assert ref.default == 'new java.util.HashSet<Boolean>()'
        assert ref.descriptor == 'io.pdef.descriptors.Descriptors.set(io.pdef.descriptors.Descriptors.bool)'

    def test_map(self):
        map0 = Map(NativeType.STRING, NativeType.FLOAT)
        ref = jreference(map0)

        assert ref.name == 'java.util.Map<String, Float>'
        assert ref.default == 'new java.util.HashMap<String, Float>()'
        assert ref.descriptor == 'io.pdef.descriptors.Descriptors.map(io.pdef.descriptors.Descriptors.string, io.pdef.descriptors.Descriptors.float0)'

    def test_enum(self):
        enum = Enum('Number')

        module = Module('test.module', definitions=[enum])
        module.link()

        ref = jreference(enum)
        assert ref.name == 'test.module.Number'
        assert ref.descriptor == 'test.module.Number.DESCRIPTOR'

    def test_enum_value(self):
        enum = Enum('Number')
        one = enum.create_value('ONE')

        module = Module('test.module', definitions=[enum])
        module.link()

        ref = jreference(one)
        assert ref.name == 'test.module.Number.ONE'
        assert ref.descriptor is None

    def test_message(self):
        msg = Message('Message')

        module = Module('test.module', definitions=[msg])
        module.link()

        ref = jreference(msg)
        assert ref.name == 'test.module.Message'
        assert ref.default == 'new test.module.Message()'
        assert ref.descriptor == 'test.module.Message.DESCRIPTOR'

    def test_interface(self):
        iface = Interface('Interface')

        module = Module('test.module', definitions=[iface])
        module.link()

        ref = jreference(iface)
        assert ref.name == 'test.module.Interface'
        assert ref.descriptor == 'test.module.Interface.DESCRIPTOR'
        assert ref.default is None

    def test_namespace__string(self):
        namespace = jnamespace({'service': 'com.company.service'})
        ref = jreference('service.client.tests', namespace)

        assert ref == 'com.company.service.client.tests'

    def test_namespace__definition(self):
        msg = Message('Message')

        module = Module('test.module', definitions=[msg])
        module.link()
        namespace = jnamespace({'test': 'com.company.test'})

        ref = jreference(msg, namespace)
        assert ref.name == 'com.company.test.module.Message'
        assert ref.descriptor == 'com.company.test.module.Message.DESCRIPTOR'
        assert ref.default == 'new com.company.test.module.Message()'
