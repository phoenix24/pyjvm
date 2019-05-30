import unittest
from .test_base import TestBase
from pyjvm.rt.models import PyVMValue, PyVMType, PyVMKonst, PyVMObject
from pyjvm.rt.klassrepo import SharedRepo
from pyjvm.utils.reader import FileReader
from pyjvm.loader.parser import PyParser


class TestPyVMValue(TestBase):

    def test_operators1(self):
        val1 = PyVMValue.pyint(10)
        val2 = PyVMValue.pyint(20)

        result = (val1 + val2)
        self.assertPyVMInt(result, 30)

        result = (val1 - val2)
        self.assertPyVMInt(result, -10)

        result = (val1 * val2)
        self.assertPyVMInt(result, 200)

        result = (val1 / val2)
        self.assertPyVMFloat(result, 0.5)

        result = (val1 // val2)
        self.assertPyVMInt(result, 0)

        result = (val2 % val1)
        self.assertPyVMInt(result, 0)

        result = (val1 % val2)
        self.assertPyVMInt(result, 10)

        result = val1 >> 1
        self.assertPyVMInt(result, 5)

        result = val1 << 1
        self.assertPyVMInt(result, 20)


class TestPyVMType(TestBase):

    def test_type(self):
        self.assertPyVMType(PyVMType.Z, 0)
        self.assertPyVMType(PyVMType.B, 1)
        self.assertPyVMType(PyVMType.S, 2)
        self.assertPyVMType(PyVMType.C, 3)
        self.assertPyVMType(PyVMType.I, 5)
        self.assertPyVMType(PyVMType.J, 6)
        self.assertPyVMType(PyVMType.F, 7)
        self.assertPyVMType(PyVMType.D, 8)
        self.assertPyVMType(PyVMType.A, 9)


class TestPyVMKonst(TestBase):

    def test_konstants(self):
        self.assertEqual(PyVMKonst.ACC_PUBLIC,      0x0001)
        self.assertEqual(PyVMKonst.ACC_PRIVATE,     0x0002)
        self.assertEqual(PyVMKonst.ACC_PROTECTED,   0x0004)
        self.assertEqual(PyVMKonst.ACC_STATIC,      0x0008)
        self.assertEqual(PyVMKonst.ACC_FINAL,       0x0010)
        self.assertEqual(PyVMKonst.ACC_SUPER,       0x0020)
        self.assertEqual(PyVMKonst.ACC_VOLATILE,    0x0040)
        self.assertEqual(PyVMKonst.ACC_TRANSIENT,   0x0080)
        self.assertEqual(PyVMKonst.ACC_INTERFACE,   0x0200)
        self.assertEqual(PyVMKonst.ACC_ABSTRACT,    0x0400)
        self.assertEqual(PyVMKonst.ACC_SYNTHETIC,   0x1000)
        self.assertEqual(PyVMKonst.ACC_ANNOTATION,  0x2000)
        self.assertEqual(PyVMKonst.ACC_ENUM,        0x4000)

        self.assertEqual(PyVMKonst.ACC_STRICT,       0x0800)
        self.assertEqual(PyVMKonst.ACC_NATIVE,       0x0100)
        self.assertEqual(PyVMKonst.ACC_BRIDGE,       0x0040)
        self.assertEqual(PyVMKonst.ACC_VARARGS,      0x0080)
        self.assertEqual(PyVMKonst.ACC_ABSTRACT_M,   0x0400)
        self.assertEqual(PyVMKonst.ACC_SYNCHRONIZED, 0x0020)


class TestPyVMObject(TestBase):

    def setUp(self):
        bytecode = FileReader.read("java/HelloWorld.class")
        parser = PyParser(bytecode).parse()
        self.pyklass = parser.build()

    def test_new(self):
        o = PyVMObject.new(self.pyklass, 0x2)
        self.assertEqual(o._id, 0x2)
        self.assertEqual(o._klass.name, 'HelloWorld')
        self.assertListEqual(o._fields, [None])

    def test_get_set_field(self):
        fields = self.pyklass.fields
        name, body = 'greeting', fields['greeting']
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[name], body)

        o = PyVMObject.new(self.pyklass, 0x2)
        self.assertIsNone(o.get_field(body))

        o.set_field(body, 0x1)
        self.assertEqual(o.get_field(body), 0x1)

