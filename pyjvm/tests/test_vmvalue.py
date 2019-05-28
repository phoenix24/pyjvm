import unittest
from pyjvm.rt.models import PyVMValue, PyVMType


class TestPyVMValue(unittest.TestCase):

    def test_operators1(self):
        val1 = PyVMValue.pyint(10)
        val2 = PyVMValue.pyint(20)

        result = (val1 + val2)
        self.assertEqual(result.type, PyVMType.I)
        self.assertEqual(result.value, 30)

        result = (val1 - val2)
        self.assertEqual(result.type, PyVMType.I)
        self.assertEqual(result.value, -10)

        result = (val1 * val2)
        self.assertEqual(result.type, PyVMType.I)
        self.assertEqual(result.value, 200)

        result = (val1 / val2)
        self.assertEqual(result.type, PyVMType.I)
        self.assertEqual(result.value, 0.5)

        result = (val1 % val2)
        self.assertEqual(result.type, PyVMType.I)
        self.assertEqual(result.value, 10)

        result = (val2 % val1)
        self.assertEqual(result.type, PyVMType.I)
        self.assertEqual(result.value, 0)

        result = (val1 // val2)
        self.assertEqual(result.type, PyVMType.I)
        self.assertEqual(result.value, 0)

        result = val1 << 1
        self.assertEqual(result.type, PyVMType.I)
        self.assertEqual(result.value, 20)

        result = val1 >> 1
        self.assertEqual(result.type, PyVMType.I)
        self.assertEqual(result.value, 5)

