import unittest
from .test_base import TestBase
from pyjvm.rt.models import PyVMObject
from pyjvm.rt.objheap import SimpleHeap
from pyjvm.utils.reader import FileReader
from pyjvm.loader.parser import PyParser


class TestObjHeap(TestBase):

    def setUp(self):
        bytecode = FileReader.read("java/HelloWorld.class")
        parser = PyParser(bytecode).parse()
        self.pyklass = parser.build()

    def test_gc(self):
        theap = SimpleHeap()
        self.assertEqual(theap.counter, 0)
        self.assertDictEqual(theap.heap, {})

        theap.gc()
        self.assertEqual(theap.counter, 0)
        self.assertDictEqual(theap.heap, {})

    def test_allocate(self):
        theap = SimpleHeap()
        index = theap.allocate(self.pyklass)
        self.assertEqual(index, 1)
        self.assertEqual(theap.counter, 1)

        index = theap.allocate(self.pyklass)
        self.assertEqual(index, 2)
        self.assertEqual(theap.counter, 2)

        actual = theap.find(index)
        expected = PyVMObject(0x2, self.pyklass)
        self.assertEqual(actual, expected)

