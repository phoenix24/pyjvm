import unittest
from .test_base import TestBase
from pyjvm.rt.models import PyVMValue, PyVMType


class TestPyVMValue(TestBase):

    def test_operators1(self):
        val1 = PyVMValue.pyint(10)
        val2 = PyVMValue.pyint(20)

        result = (val1 + val2)
        self.assertPyVMInt(result, 30)

        result = (val1 - val2)
        self.assertPyVMInt(result, -10)

        result = (val1 * val2)
        self.assertPyVMInt(result, 200)

        result = (val1 / val2)
        self.assertPyVMFloat(result, 0.5)

        result = (val1 // val2)
        self.assertPyVMInt(result, 0)

        result = (val2 % val1)
        self.assertPyVMInt(result, 0)

        result = (val1 % val2)
        self.assertPyVMInt(result, 10)

        result = val1 >> 1
        self.assertPyVMInt(result, 5)

        result = val1 << 1
        self.assertPyVMInt(result, 20)

