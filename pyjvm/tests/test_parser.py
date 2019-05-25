import unittest
from pyjvm.utils.reader import FileReader
from pyjvm.loader.parser import PyParser


class TestParser(unittest.TestCase):

    def setUp(self):
        bytecode = FileReader.read("java/SampleInvoke.class")
        self.parser = PyParser(bytecode).parse()

    def test_parser1(self):
        pass

    def test_parser2(self):
        pass

    def test_parser3(self):
        pass
