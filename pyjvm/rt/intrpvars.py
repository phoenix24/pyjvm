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