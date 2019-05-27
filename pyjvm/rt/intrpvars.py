from pyjvm.rt.models import PyVMValue


class IntrptVars(object):
    def __init__(self, args=None):
        self.args = args or [None] * 256

    def __str__(self) -> str:
        return "IntrptVars(args={})".format(self.args)

    def __repr__(self) -> str:
        return self.__str__()

    def iload(self, index: int) -> PyVMValue:
        return self.args[index].copy()

    def store(self, index: int, value: PyVMValue) -> None:
        self.args[index] = value

    def dload(self, index: int):
        p1 = self.args[index].copy()
        p2 = self.args[index + 1].copy()
        return PyVMValue.pydouble((p1.value << 8) + p2.value)

    def iinc(self, offset, amount):
        var = self.args[offset & 0xff]
        self.args[offset & 0xff] = PyVMValue.pyint(var.value + amount)
