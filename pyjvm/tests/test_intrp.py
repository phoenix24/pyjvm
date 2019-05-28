import unittest
from .test_base import TestBase
from pyjvm.rt.models import PyVMValue, PyVMType
from pyjvm.rt.intrptr import Intrptr
from pyjvm.rt.intrpvars import IntrptVars
from pyjvm.rt.klassrepo import SharedRepo
from pyjvm.utils.reader import FileReader
from pyjvm.loader.parser import PyParser


class TestInterptrSampleInvoke(TestBase):

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
        self.assertPyVMInt(result, 7)

    def test_foo(self):
        method = self.pyklass.get_method("foo:()I")
        self.assertEqual(method.signature, '()I')
        self.assertEqual(method.num_params, 0)

        result = self.intrptr.execute(method)
        self.assertPyVMInt(result, 19)

    def test_too(self):
        method = self.pyklass.get_method("too:()I")
        self.assertEqual(method.signature, '()I')
        self.assertEqual(method.num_params, 0)

        result = self.intrptr.execute(method)
        self.assertPyVMInt(result, 26)


class TestInterptrSampleIntTest(TestBase):

    def setUp(self):
        bytecode = FileReader.read("java/SampleInvoke1.class")
        parser = PyParser(bytecode).parse()
        self.pyklass = parser.build()
        repo = SharedRepo()
        repo.add(klass=self.pyklass)
        self.intrptr = Intrptr(repo)

    def test_two(self):
        method = self.pyklass.get_method("two:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(1),
            PyVMValue.pyint(3),
        ]))
        self.assertPyVMInt(result, 4)

        # pass other vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(100),
            PyVMValue.pyint(300),
        ]))
        self.assertPyVMInt(result, 400)

    def test_twod(self):
        method = self.pyklass.get_method("twod:()I")
        self.assertEqual(method.signature, '()I')
        self.assertEqual(method.num_params, 0)

        result = self.intrptr.execute(method)
        self.assertPyVMInt(result, 4)

    def test_mul(self):
        method = self.pyklass.get_method("mul:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(2),
            PyVMValue.pyint(3),
        ]))
        self.assertPyVMInt(result, 6)

    def test_div(self):
        method = self.pyklass.get_method("div:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(20),
            PyVMValue.pyint(5),
        ]))
        self.assertPyVMInt(result, 4)

    def test_rem(self):
        method = self.pyklass.get_method("rem:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(20),
            PyVMValue.pyint(3),
        ]))
        self.assertPyVMInt(result, 2)

    def test_sub(self):
        method = self.pyklass.get_method("sub:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(20),
            PyVMValue.pyint(5),
        ]))
        self.assertPyVMInt(result, 15)

    def test_inc1(self):
        method = self.pyklass.get_method("inc1:(I)I")
        self.assertEqual(method.signature, '(I)I')
        self.assertEqual(method.num_params, 1)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(5),
        ]))
        self.assertPyVMInt(result, 5)

    def test_inc2(self):
        method = self.pyklass.get_method("inc2:(I)I")
        self.assertEqual(method.signature, '(I)I')
        self.assertEqual(method.num_params, 1)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(5),
        ]))
        self.assertPyVMInt(result, 6)

    def test_neg(self):
        method = self.pyklass.get_method("neg:(I)I")
        self.assertEqual(method.signature, '(I)I')
        self.assertEqual(method.num_params, 1)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(5),
        ]))
        self.assertPyVMInt(result, -5)

    def test_or(self):
        method = self.pyklass.get_method("or:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(20),
            PyVMValue.pyint(5),
        ]))
        self.assertPyVMInt(result, 21)

    def test_and(self):
        method = self.pyklass.get_method("and:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(20),
            PyVMValue.pyint(5),
        ]))
        self.assertPyVMInt(result, 4)

    def test_calc1(self):
        method = self.pyklass.get_method("calc1:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(15),
            PyVMValue.pyint(5),
        ]))
        self.assertPyVMInt(result, 100)

    @unittest.skip
    def test_soo(self):
        method = self.pyklass.get_method("soo:()Ljava/lang/String;")
        self.assertEqual(method.signature, '()Ljava/lang/String;')
        self.assertEqual(method.num_params, 0)

        result = self.intrptr.execute(method)
        self.assertPyVMInt(result, 4)

    def test_ifeq(self):
        method = self.pyklass.get_method("ifeq:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(4),
            PyVMValue.pyint(5),
        ]))
        self.assertPyVMInt(result, 5)

        # pass other vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(300),
            PyVMValue.pyint(100),
        ]))
        self.assertPyVMInt(result, 100)

    def test_ifleq(self):
        method = self.pyklass.get_method("ifleq:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(4),
            PyVMValue.pyint(5),
        ]))
        self.assertPyVMInt(result, 4)

        # pass other vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(300),
            PyVMValue.pyint(100),
        ]))
        self.assertPyVMInt(result, 100)

    def test_ifgeq(self):
        method = self.pyklass.get_method("ifgeq:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(4),
            PyVMValue.pyint(5),
        ]))
        self.assertPyVMInt(result, 5)

        # pass other vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(300),
            PyVMValue.pyint(100),
        ]))
        self.assertPyVMInt(result, 300)

    def test_ifelse4(self):
        method = self.pyklass.get_method("ifelse4:()I")
        self.assertEqual(method.signature, '()I')
        self.assertEqual(method.num_params, 0)

        result = self.intrptr.execute(method)
        self.assertPyVMInt(result, 4)


class TestInterptrSampleDoubleTest(TestBase):

    def setUp(self):
        bytecode = FileReader.read("java/SampleInvoke2.class")
        parser = PyParser(bytecode).parse()
        self.pyklass = parser.build()
        repo = SharedRepo()
        repo.add(klass=self.pyklass)
        self.intrptr = Intrptr(repo)

    def test_add(self):
        method = self.pyklass.get_method("add:(DD)D")
        self.assertEqual(method.signature, "(DD)D")
        self.assertEqual(method.num_params, 2)

        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(0),
            PyVMValue.pyint(3),
            PyVMValue.pyint(0),
            PyVMValue.pyint(2),
        ]))
        self.assertPyVMDouble(result, 5)

    def test_sub(self):
        method = self.pyklass.get_method("sub:(DD)D")
        self.assertEqual(method.signature, "(DD)D")
        self.assertEqual(method.num_params, 2)

        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(0),
            PyVMValue.pyint(3),
            PyVMValue.pyint(0),
            PyVMValue.pyint(2),
        ]))
        self.assertPyVMDouble(result, 1)

    def test_mul(self):
        method = self.pyklass.get_method("mul:(DD)D")
        self.assertEqual(method.signature, "(DD)D")
        self.assertEqual(method.num_params, 2)

        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(0),
            PyVMValue.pyint(3),
            PyVMValue.pyint(0),
            PyVMValue.pyint(2),
        ]))
        self.assertPyVMDouble(result, 6)

    def test_div(self):
        method = self.pyklass.get_method("div:(DD)D")
        self.assertEqual(method.signature, "(DD)D")
        self.assertEqual(method.num_params, 2)

        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(0),
            PyVMValue.pyint(3),
            PyVMValue.pyint(0),
            PyVMValue.pyint(2),
        ]))
        self.assertPyVMDouble(result, 1)

    def test_rem(self):
        method = self.pyklass.get_method("rem:(DD)D")
        self.assertEqual(method.signature, "(DD)D")
        self.assertEqual(method.num_params, 2)

        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(0),
            PyVMValue.pyint(5),
            PyVMValue.pyint(0),
            PyVMValue.pyint(3),
        ]))
        self.assertPyVMDouble(result, 2)

    def test_neg(self):
        method = self.pyklass.get_method("neg:(D)D")
        self.assertEqual(method.signature, "(D)D")
        self.assertEqual(method.num_params, 1)

        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(0),
            PyVMValue.pyint(5),
        ]))
        self.assertPyVMDouble(result, -5)

    def test_inc1(self):
        method = self.pyklass.get_method("inc1:(D)D")
        self.assertEqual(method.signature, "(D)D")
        self.assertEqual(method.num_params, 1)

        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(0),
            PyVMValue.pyint(5),
        ]))
        self.assertPyVMDouble(result, 5)

    def test_inc2(self):
        method = self.pyklass.get_method("inc2:(D)D")
        self.assertEqual(method.signature, "(D)D")
        self.assertEqual(method.num_params, 1)

        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(0),
            PyVMValue.pyint(5),
        ]))
        self.assertPyVMDouble(result, 6)
