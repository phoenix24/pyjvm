from .test_base import TestBase
from pyjvm.rt.models import PyVMValue
from pyjvm.rt.intrpstk import IntrptEvalStack


class TestEvalStack(TestBase):

    def test_push_pop(self):
        stack = IntrptEvalStack()
        self.assertEqual(stack.size(), 0)

        val = PyVMValue.pyint(10)
        stack.push(val)
        self.assertEqual(stack.size(), 1)

        val1 = stack.pop()
        self.assertEqual(val, val1)
        self.assertEqual(stack.size(), 0)

    def test_iadd(self):
        stack = IntrptEvalStack()
        stack.push(PyVMValue.pyint(10))
        stack.push(PyVMValue.pyint(20))
        self.assertEqual(stack.size(), 2)

        stack.iadd()
        self.assertEqual(stack.size(), 1)

        val = stack.pop()
        self.assertPyVMInt(val, 30)
        self.assertEqual(stack.size(), 0)

    def test_isub(self):
        stack = IntrptEvalStack()
        stack.push(PyVMValue.pyint(10))
        stack.push(PyVMValue.pyint(20))
        self.assertEqual(stack.size(), 2)

        stack.isub()
        self.assertEqual(stack.size(), 1)

        val = stack.pop()
        self.assertPyVMInt(val, -10)
        self.assertEqual(stack.size(), 0)

    def test_imul(self):
        stack = IntrptEvalStack()
        stack.push(PyVMValue.pyint(10))
        stack.push(PyVMValue.pyint(20))
        self.assertEqual(stack.size(), 2)

        stack.imul()
        self.assertEqual(stack.size(), 1)

        val = stack.pop()
        self.assertPyVMInt(val, 200)
        self.assertEqual(stack.size(), 0)

    def test_idiv(self):
        stack = IntrptEvalStack()
        stack.push(PyVMValue.pyint(10))
        stack.push(PyVMValue.pyint(20))
        self.assertEqual(stack.size(), 2)

        stack.idiv()
        self.assertEqual(stack.size(), 1)

        val = stack.pop()
        self.assertPyVMInt(val, 0)
        self.assertEqual(stack.size(), 0)

        stack.push(PyVMValue.pyint(20))
        stack.push(PyVMValue.pyint(10))
        self.assertEqual(stack.size(), 2)

        stack.idiv()
        self.assertEqual(stack.size(), 1)

        val = stack.pop()
        self.assertPyVMInt(val, 2)
        self.assertEqual(stack.size(), 0)

    def test_irem(self):
        stack = IntrptEvalStack()
        stack.push(PyVMValue.pyint(5))
        stack.push(PyVMValue.pyint(3))
        self.assertEqual(stack.size(), 2)

        stack.irem()
        self.assertEqual(stack.size(), 1)

        val = stack.pop()
        self.assertPyVMInt(val, 2)
        self.assertEqual(stack.size(), 0)

        stack.push(PyVMValue.pyint(3))
        stack.push(PyVMValue.pyint(5))
        self.assertEqual(stack.size(), 2)

        stack.irem()
        self.assertEqual(stack.size(), 1)

        val = stack.pop()
        self.assertPyVMInt(val, 3)
        self.assertEqual(stack.size(), 0)

    def test_ior(self):
        stack = IntrptEvalStack()
        stack.push(PyVMValue.pyint(6))
        stack.push(PyVMValue.pyint(8))
        self.assertEqual(stack.size(), 2)

        stack.ior()
        self.assertEqual(stack.size(), 1)

        val = stack.pop()
        self.assertPyVMInt(val, 14)
        self.assertEqual(stack.size(), 0)

    def test_ineg(self):
        stack = IntrptEvalStack()
        stack.push(PyVMValue.pyint(10))
        stack.push(PyVMValue.pyint(20))
        self.assertEqual(stack.size(), 2)

        stack.ineg()
        self.assertEqual(stack.size(), 2)

        val = stack.pop()
        self.assertPyVMInt(val, -20)
        self.assertEqual(stack.size(), 1)

    def test_iconst(self):
        stack = IntrptEvalStack()
        stack.iconst(10)
        self.assertEqual(stack.size(), 1)

        val = stack.pop()
        self.assertPyVMInt(val, 10)
        self.assertEqual(stack.size(), 0)

