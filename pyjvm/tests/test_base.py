import unittest
from pyjvm.rt.models import PyVMValue, PyVMType


class TestBase(unittest.TestCase):

    def assertValue(self, actual: PyVMValue, expected: PyVMValue) -> None:
        self.assertEqual(actual.type, expected.type)
        self.assertEqual(actual.value, expected.value)

    def assertPyVMInt(self, actual: PyVMValue, expected: int) -> None:
        self.assertValue(actual, PyVMValue.pyint(expected))

    def assertPyVMFloat(self, actual: PyVMValue, expected: float) -> None:
        self.assertValue(actual, PyVMValue.pyfloat(expected))

    def assertPyVMDouble(self, actual: PyVMValue, expected: float) -> None:
        self.assertValue(actual, PyVMValue.pydouble(expected))
