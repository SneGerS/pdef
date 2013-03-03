# encoding: utf-8
import unittest
from pdef.lang import *
from pdef.java import *


class TestJavaRef(unittest.TestCase):
    def setUp(self):
        ref = JavaRef('Map')
        ref.package = 'java.lang'
        ref.variables = [JavaRef('K'), JavaRef('V')]
        self.ref = ref

    def test(self):
        assert str(self.ref) == 'java.lang.Map<K, V>'

    def test_local(self):
        assert str(self.ref.local) == 'Map<K, V>'

    def test_raw(self):
        assert str(self.ref.raw) == 'java.lang.Map'

    def test_wildcard(self):
        assert str(self.ref.wildcard) == 'java.lang.Map<K, V>'

    def test_boxed(self):
        assert str(self.ref) == str(self.ref.boxed)


class TestVariableJavaRef(unittest.TestCase):
    def setUp(self):
        var = Variable('T')
        msg = Message('Class')
        msg.add_variables(var)
        self.ref = VariableJavaRef(var)

    def test(self):
        assert str(self.ref) == 'T'

    def test_local(self):
        assert str(self.ref) == str(self.ref.local)

    def test_raw(self):
        assert str(self.ref) == str(self.ref.raw)

    def test_boxed(self):
        assert str(self.ref) == str(self.ref.boxed)

    def test_wildcard(self):
        assert str(self.ref.wildcard) == '?'

    def test_descriptor(self):
        assert str(self.ref.descriptor) == 'variableT'


class TestTypeJavaRef(unittest.TestCase):
    def setUp(self):
        msg = Message('Message', variables=[Variable('T')])
        module = Module('module')
        module.add_definitions(msg)
        self.ref = TypeJavaRef(msg)

    def test(self):
        assert str(self.ref) == 'module.Message<T>'

    def test_local(self):
        ref = self.ref.local
        assert str(ref) == 'Message<T>'

    def test_raw(self):
        ref = self.ref.raw
        assert str(ref) == 'module.Message'

    def test_boxed(self):
        assert str(self.ref) == str(self.ref.boxed)

    def test_wildcard(self):
        ref = self.ref.wildcard
        assert str(ref) == 'module.Message<?>'

    def test_local_wildcard(self):
        ref = self.ref.local.wildcard
        assert str(ref) == 'Message<?>'

    def test_descriptor(self):
        assert self.ref.descriptor == 'module.Message.getClassDescriptor()'

    def test_default(self):
        assert self.ref.default == 'null'


class TestNativeJavaRef(unittest.TestCase):
    descriptor = 'pdef.provided.NativeListDescriptor.getInstance()'
    default = 'com.google.common.collect.ImmutableList.of()'
    def setUp(self):
        native = Native('List', variables=[Variable('T')], options=NativeOptions(
            java_type='java.lang.List',
            java_boxed='java.lang.List',
            java_descriptor=self.descriptor,
            java_default=self.default))
        self.ref = NativeJavaRef(native)

    def test(self):
        assert str(self.ref) == 'java.lang.List<T>'

    def test_local(self):
        assert str(self.ref.local) == 'java.lang.List<T>'

    def test_raw(self):
        assert str(self.ref.raw) == 'java.lang.List'

    def test_boxed(self):
        assert str(self.ref.boxed) == 'java.lang.List<T>'

    def test_wildcard(self):
        assert str(self.ref.wildcard) == 'java.lang.List<?>'

    def test_local_wildcard(self):
        assert str(self.ref.local.wildcard) == 'java.lang.List<?>'

    def test_descriptor(self):
        assert str(self.ref.descriptor) == self.descriptor

    def test_default(self):
        assert str(self.ref.default) == self.default