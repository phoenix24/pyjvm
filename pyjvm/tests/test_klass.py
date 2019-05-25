import unittest
from pyjvm.utils.reader import FileReader
from pyjvm.loader.parser import PyParser


class TestKlass(unittest.TestCase):

    def setUp(self):
        bytecode = FileReader.read("java/SampleInvoke.class")
        parser = PyParser(bytecode).parse()
        self.pyklass = parser.build()

    def test_klass1(self):
        pass

    def test_klass2(self):
        pass

    def test_klass3(self):
        pass

        

    