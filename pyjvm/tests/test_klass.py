import unittest
from .test_base import TestBase
from pyjvm.utils.reader import FileReader
from pyjvm.loader.parser import PyParser


class TestKlass1(TestBase):

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


class TestKlass2(TestBase):

    def setUp(self):
        bytecode = FileReader.read("java/HelloWorld.class")
        parser = PyParser(bytecode).parse()
        self.pyklass = parser.build()

    def test_items(self):
        items = self.pyklass.items
        self.assertDictEqual(items, {})

    def test_fields(self):
        fields = self.pyklass.get_fields()
        self.assertEqual(1, len(fields))
        self.assertListEqual(fields, ['answer'])

    def test_methods(self):
        methods = self.pyklass.get_methods()
        self.assertEqual(len(methods), 4)
        self.assertListEqual(methods, [
            '<init>:()V',
            'add:(II)I',
            'multiply:(I)I',
            'compute:()I',
        ])

    def test_method_by_index(self):
        methods = self.pyklass.methods
        self.assertEqual(len(methods), 4)

        methodsIdx = self.pyklass.methodsByIndex
        self.assertEqual(len(methodsIdx), 2)

        self.assertEqual(methodsIdx[3], 'HelloWorld.add:(II)I')
        self.assertEqual(methodsIdx[1], 'java/lang/Object.<init>:()V')
