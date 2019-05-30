from typing import List
from pyjvm.rt.models import PyVMValue

Args = List[PyVMValue]


class IntrptVars(object):
    def __init__(self, args=None):
        self.args:Args = args or [None] * 256

    def __str__(self) -> str:
        return "IntrptVars(args={})".format(self.args)

    def __repr__(self) -> str:
        return self.__str__()

    def iload(self, index: int) -> PyVMValue:
        pyvalue: PyVMValue = self.args[index]
        return pyvalue.clone()

    def store(self, index: int, value: PyVMValue) -> None:
        self.args[index] = value

    def dload(self, index: int):
        p1: PyVMValue = self.args[index].clone()
        p2: PyVMValue = self.args[index + 1].clone()
        return PyVMValue.pydouble((p1.value << 8) + p2.value)

    def iinc(self, offset, amount):
        var = self.args[offset & 0xff]
        self.args[offset & 0xff] = PyVMValue.pyint(var.value + amount)

    def aload(self, index: int) -> PyVMValue:
        pyvalue: PyVMValue = self.args[index]
        return pyvalue.clone()

    def astore(self, index: int, value: PyVMValue) -> None:
        self.args[index] = value
