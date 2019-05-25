import unittest
from pyjvm.rt.models import PyVMValue, PyVMType
from pyjvm.rt.intrptr import Intrptr
from pyjvm.rt.klassrepo import SharedRepo
from pyjvm.utils.reader import FileReader
from pyjvm.loader.parser import PyParser


class TestInterptr(unittest.TestCase):

    def setUp(self):
        bytecode = FileReader.read("java/SampleInvoke.class")
        parser = PyParser(bytecode).parse()
        self.pyklass = parser.build()
        repo = SharedRepo()
        repo.add(klass=self.pyklass)
        self.intrptr = Intrptr(repo)

    def test_bar(self):
        method = self.pyklass.get_method("bar:()I")
        result = self.intrptr.execute(method)
        self.assertEqual(result.value, 7)
        self.assertEqual(result.type, PyVMType.I)

    def test_foo(self):
        method = self.pyklass.get_method("foo:()I")
        result = self.intrptr.execute(method)
        self.assertEqual(result.value, 19)
        self.assertEqual(result.type, PyVMType.I)

    def test_too(self):
        method = self.pyklass.get_method("too:()I")
        result = self.intrptr.execute(method)
        self.assertEqual(result.value, 26)
        self.assertEqual(result.type, PyVMType.I)

    @unittest.skip("TODO: need support for passing params")
    def test_two(self):
        method = self.pyklass.get_method("two:()I")
        result = self.intrptr.execute(method)
        self.assertEqual(result.value, 26)
        self.assertEqual(result.type, PyVMType.I)
