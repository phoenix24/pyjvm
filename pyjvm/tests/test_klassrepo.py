import unittest
from .test_base import TestBase
from pyjvm.rt.models import PyVMField, PyVMType, PyVMMethod
from pyjvm.rt.klassrepo import SharedRepo
from pyjvm.utils.reader import FileReader
from pyjvm.loader.parser import PyParser


class TestKlassRepo(TestBase):

    def setUp(self):
        bytecode = FileReader.read("java/HelloWorld.class")
        parser = PyParser(bytecode).parse()
        self.pyklass = parser.build()

    def test_add_repo(self):
        repo = SharedRepo()
        repo.add(klass=self.pyklass)

        expected = {
            'HelloWorld': self.pyklass,
            'java/lang/Object': SharedRepo.OBJECT_CLASS
        }
        self.assertDictEqual(repo.klass_cache, expected)

        expected = {
            'HelloWorld.add:(II)I': self.pyklass.get_method('add:(II)I'),
            'HelloWorld.<init>:()V': self.pyklass.get_method('<init>:()V'),
            'HelloWorld.compute:()I': self.pyklass.get_method('compute:()I'),
            'HelloWorld.multiply:(I)I': self.pyklass.get_method('multiply:(I)I'),
        }
        self.assertDictEqual(repo.method_cache, expected)

        expected = {
          'HelloWorld.answer:I': PyVMField(self.pyklass, 'answer', PyVMType.I, flags=2)
        }
        self.assertDictEqual(repo.field_cache, expected)

    def test_lookup_klass_object(self):
        repo = SharedRepo()
        repo.add(klass=self.pyklass)
        klass = repo.lookupKlass('HelloWorld', 5)
        self.assertEqual(klass, SharedRepo.OBJECT_CLASS)

    def test_lookup_klass_helloworld(self):
        repo = SharedRepo()
        repo.add(klass=self.pyklass)
        klass = repo.lookupKlass('HelloWorld', 4)
        self.assertEqual(klass, self.pyklass)

    def test_lookup_field(self):
        repo = SharedRepo()
        repo.add(klass=self.pyklass)

        field = repo.lookupField('HelloWorld', 2)
        expected = PyVMField(self.pyklass, 'answer', PyVMType.I, 2)
        self.assertEqual(field, expected)

    def test_lookup_method_exact(self):
        repo = SharedRepo()
        repo.add(klass=self.pyklass)

        method = repo.lookupMethodExact('HelloWorld', 3)
        expected = PyVMMethod(self.pyklass, '(II)I', 'add:(II)I', [b'\x1b', b'\x1c', b'`', b'\xac'], 1)
        self.assertEqual(method, expected)

    @unittest.skip
    def test_lookup_method_virtual(self):
        pass



