import unittest
from .test_base import TestBase
from pyjvm.utils.reader import FileReader
from pyjvm.loader.parser import PyParser


class TestKlass(TestBase):

    def setUp(self):
        bytecode = FileReader.read("java/SampleInvoke.class")
        parser = PyParser(bytecode).parse()
        self.pyklass = parser.build()

    def test_items(self):
        items = self.pyklass.items
        self.assertDictEqual(items, {})

    def test_fields(self):
        fields = self.pyklass.get_fields()
        self.assertEqual(1, len(fields))
        self.assertListEqual(fields, ['greeting'])

    def test_methods(self):
        methods = self.pyklass.get_methods()
        self.assertEqual(len(methods), 6)
        self.assertListEqual(methods, [
            '<init>:()V',
            'bar:()I',
            'foo:()I',
            'too:()I',
            'two:(II)I',
            'main:([Ljava/lang/String;)V',
        ])

    def test_method_foo(self):
        methods = self.pyklass.get_methods()
        self.assertEqual(len(methods), 6)
        self.assertEqual(methods[2], 'foo:()I')
