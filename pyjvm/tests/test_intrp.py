import unittest
from pyjvm.rt.models import PyVMValue, PyVMType
from pyjvm.rt.intrptr import Intrptr
from pyjvm.rt.klassrepo import SharedRepo
from pyjvm.utils.reader import FileReader
from pyjvm.loader.parser import PyParser


class TestInterptrSampleInvoke(unittest.TestCase):

    def setUp(self):
        bytecode = FileReader.read("java/SampleInvoke.class")
        parser = PyParser(bytecode).parse()
        self.pyklass = parser.build()
        repo = SharedRepo()
        repo.add(klass=self.pyklass)
        self.intrptr = Intrptr(repo)

    def test_bar(self):
        method = self.pyklass.get_method("bar:()I")
        self.assertEqual(method.signature, '()I')
        self.assertEqual(method.num_params, 0)

        result = self.intrptr.execute(method)
        self.assertEqual(result.value, 7)
        self.assertEqual(result.type, PyVMType.I)

    def test_foo(self):
        method = self.pyklass.get_method("foo:()I")
        self.assertEqual(method.signature, '()I')
        self.assertEqual(method.num_params, 0)

        result = self.intrptr.execute(method)
        self.assertEqual(result.value, 19)
        self.assertEqual(result.type, PyVMType.I)

    def test_too(self):
        method = self.pyklass.get_method("too:()I")
        self.assertEqual(method.signature, '()I')
        self.assertEqual(method.num_params, 0)

        result = self.intrptr.execute(method)
        self.assertEqual(result.value, 26)
        self.assertEqual(result.type, PyVMType.I)


class TestInterptrSampleInvokeTest(unittest.TestCase):

    def setUp(self):
        bytecode = FileReader.read("java/SampleInvoke1.class")
        parser = PyParser(bytecode).parse()
        self.pyklass = parser.build()
        repo = SharedRepo()
        repo.add(klass=self.pyklass)
        self.intrptr = Intrptr(repo)

    def test_two(self):
        method = self.pyklass.get_method("twod:()I")
        self.assertEqual(method.signature, '()I')
        self.assertEqual(method.num_params, 0)

        result = self.intrptr.execute(method)
        self.assertEqual(result.value, 4)
        self.assertEqual(result.type, PyVMType.I)
