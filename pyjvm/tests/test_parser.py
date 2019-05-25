import unittest
from pyjvm.rt.models import PyVMType
from pyjvm.klass.models import PyField, PyMethod
from pyjvm.utils.reader import FileReader
from pyjvm.loader.parser import PyParser


class TestParser(unittest.TestCase):

    def setUp(self):
        self.bytecode = FileReader.read("java/SampleInvoke.class")

    def test_kptable(self):
        parser = PyParser(self.bytecode).parse()
        kptable = parser.kptable
        self.assertEqual(len(kptable), 14)
        self.assertEqual(kptable[1].type, "UTF8")
        self.assertEqual(kptable[3].type, "INTEGER")
        self.assertEqual(kptable[4].type, "FLOAT")
        self.assertEqual(kptable[5].type, "LONG")
        self.assertEqual(kptable[6].type, "DOUBLE")
        self.assertEqual(kptable[7].type, "CLASS")
        self.assertEqual(kptable[8].type, "STRING")
        self.assertEqual(kptable[9].type, "FIELDREF")
        self.assertEqual(kptable[10].type, "METHODREF")
        self.assertEqual(kptable[11].type, "INTERFACE_METHODREF")
        self.assertEqual(kptable[12].type, "NAMEANDTYPE")
        self.assertEqual(kptable[15].type, "METHODHANDLE")
        self.assertEqual(kptable[16].type, "METHODTYPE")
        self.assertEqual(kptable[18].type, "INVOKEDYNAMIC")

    def test_header(self):
        parser = PyParser(self.bytecode)
        parser._init()
        parser._header()
        self.assertEqual(parser.minor, 0)
        self.assertEqual(parser.major, 52)
        self.assertEqual(parser.offset, 10)
        self.assertEqual(parser.pool_count, 30)
        self.assertEqual(parser.pool_items, [])

    def test_constant_pool(self):
        parser = PyParser(self.bytecode)
        parser._init()
        parser._header()
        parser._constant_pool()

    def test_basic_type_info(self):
        parser = PyParser(self.bytecode)
        parser._init()
        parser._header()
        parser._constant_pool()
        parser._basic_type_info()
        self.assertEqual(parser.offset, 297)
        self.assertEqual(parser.flags, 33)
        self.assertEqual(parser.klass, 'SampleInvoke')
        self.assertEqual(parser.klassIdx, 4)
        self.assertEqual(parser.super, 'java/lang/Object')
        self.assertEqual(parser.superIdx, 5)
        self.assertEqual(parser.interfaces, [])

    def test_fields(self):
        parser = PyParser(self.bytecode)
        parser._init()
        parser._header()
        parser._constant_pool()
        parser._basic_type_info()
        parser._fields()
        self.assertEqual(parser.offset, 315)
        self.assertEqual(len(parser.fields), 1)
        self.assertEqual(parser.fields[0], PyField(
            'SampleInvoke', 26, 'greeting', 6, PyVMType.A, 7
        ))

    def test_methods(self):
        parser = PyParser(self.bytecode)
        parser._init()
        parser._header()
        parser._constant_pool()
        parser._basic_type_info()
        parser._fields()
        parser._methods()
        self.assertEqual(parser.offset, 593)
        self.assertEqual(len(parser.methods), 6)
        self.assertEqual(parser.methods[0], PyMethod(
            'SampleInvoke', 1, 10, '<init>', 11, '()V'
        ))
