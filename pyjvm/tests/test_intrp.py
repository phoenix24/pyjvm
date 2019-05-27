import unittest
from pyjvm.rt.models import PyVMValue, PyVMType
from pyjvm.rt.intrptr import Intrptr
from pyjvm.rt.intrpvars import IntrptVars
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
        method = self.pyklass.get_method("two:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(1),
            PyVMValue.pyint(3),
        ]))
        self.assertEqual(result.value, 4)
        self.assertEqual(result.type, PyVMType.I)

        # pass other vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(100),
            PyVMValue.pyint(300),
        ]))
        self.assertEqual(result.value, 400)
        self.assertEqual(result.type, PyVMType.I)

    def test_twod(self):
        method = self.pyklass.get_method("twod:()I")
        self.assertEqual(method.signature, '()I')
        self.assertEqual(method.num_params, 0)

        result = self.intrptr.execute(method)
        self.assertEqual(result.value, 4)
        self.assertEqual(result.type, PyVMType.I)

    def test_mul(self):
        method = self.pyklass.get_method("mul:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(2),
            PyVMValue.pyint(3),
        ]))
        self.assertEqual(result.value, 6)
        self.assertEqual(result.type, PyVMType.I)

    def test_div(self):
        method = self.pyklass.get_method("div:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(20),
            PyVMValue.pyint(5),
        ]))
        self.assertEqual(result.value, 4)
        self.assertEqual(result.type, PyVMType.I)

    def test_rem(self):
        method = self.pyklass.get_method("rem:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(20),
            PyVMValue.pyint(3),
        ]))
        self.assertEqual(result.value, 2)
        self.assertEqual(result.type, PyVMType.I)

    def test_sub(self):
        method = self.pyklass.get_method("sub:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(20),
            PyVMValue.pyint(5),
        ]))
        self.assertEqual(result.value, 15)
        self.assertEqual(result.type, PyVMType.I)

    def test_inc1(self):
        method = self.pyklass.get_method("inc1:(I)I")
        self.assertEqual(method.signature, '(I)I')
        self.assertEqual(method.num_params, 1)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(5),
        ]))
        self.assertEqual(result.value, 5)
        self.assertEqual(result.type, PyVMType.I)

    def test_inc2(self):
        method = self.pyklass.get_method("inc2:(I)I")
        self.assertEqual(method.signature, '(I)I')
        self.assertEqual(method.num_params, 1)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(5),
        ]))
        self.assertEqual(result.value, 6)
        self.assertEqual(result.type, PyVMType.I)

    def test_neg(self):
        method = self.pyklass.get_method("neg:(I)I")
        self.assertEqual(method.signature, '(I)I')
        self.assertEqual(method.num_params, 1)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(5),
        ]))
        self.assertEqual(result.value, -5)
        self.assertEqual(result.type, PyVMType.I)

    def test_or(self):
        method = self.pyklass.get_method("or:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(20),
            PyVMValue.pyint(5),
        ]))
        self.assertEqual(result.value, 21)
        self.assertEqual(result.type, PyVMType.I)

    def test_and(self):
        method = self.pyklass.get_method("and:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(20),
            PyVMValue.pyint(5),
        ]))
        self.assertEqual(result.value, 4)
        self.assertEqual(result.type, PyVMType.I)

    def test_calc1(self):
        method = self.pyklass.get_method("calc1:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars([
            PyVMValue.pyint(15),
            PyVMValue.pyint(5),
        ]))
        self.assertEqual(result.value, 100)
        self.assertEqual(result.type, PyVMType.I)

    @unittest.skip
    def test_soo(self):
        method = self.pyklass.get_method("soo:()Ljava/lang/String;")
        self.assertEqual(method.signature, '()Ljava/lang/String;')
        self.assertEqual(method.num_params, 0)

        result = self.intrptr.execute(method)
        self.assertEqual(result.value, 4)
        self.assertEqual(result.type, PyVMType.I)

    def test_ifeq(self):
        method = self.pyklass.get_method("ifeq:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(4),
            PyVMValue.pyint(5),
        ]))

        self.assertEqual(result.value, 5)
        self.assertEqual(result.type, PyVMType.I)

        # pass other vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(300),
            PyVMValue.pyint(100),
        ]))
        self.assertEqual(result.value, 100)
        self.assertEqual(result.type, PyVMType.I)

    def test_ifleq(self):
        method = self.pyklass.get_method("ifleq:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(4),
            PyVMValue.pyint(5),
        ]))

        self.assertEqual(result.value, 4)
        self.assertEqual(result.type, PyVMType.I)

        # pass other vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(300),
            PyVMValue.pyint(100),
        ]))
        self.assertEqual(result.value, 100)
        self.assertEqual(result.type, PyVMType.I)

    def test_ifgeq(self):
        method = self.pyklass.get_method("ifgeq:(II)I")
        self.assertEqual(method.signature, '(II)I')
        self.assertEqual(method.num_params, 2)

        # pass function body vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(4),
            PyVMValue.pyint(5),
        ]))

        self.assertEqual(result.value, 5)
        self.assertEqual(result.type, PyVMType.I)

        # pass other vars.
        result = self.intrptr.execute(method, IntrptVars(args=[
            PyVMValue.pyint(300),
            PyVMValue.pyint(100),
        ]))
        self.assertEqual(result.value, 300)
        self.assertEqual(result.type, PyVMType.I)

    def test_ifelse4(self):
        print(self.pyklass.methods)
        method = self.pyklass.get_method("ifelse4:()I")
        self.assertEqual(method.signature, '()I')
        self.assertEqual(method.num_params, 0)

        result = self.intrptr.execute(method)
        self.assertEqual(result.value, 4)
        self.assertEqual(result.type, PyVMType.I)
