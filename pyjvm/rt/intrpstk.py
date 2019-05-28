from .models import PyVMValue, PyVMType
from typing import List, Dict, Sequence, Mapping


class IntrptEvalStack(object):
    def __init__(self):
        self.stack: List[PyVMValue] = []

    def aconst_null(self):
        self.stack.append(PyVMValue(PyVMType.A, 0))

    def iadd(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        result = val1.value + val2.value
        pyvalue = PyVMValue.pyint(result)
        self.stack.append(pyvalue)

    def isub(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        result = val2.value - val1.value
        pyvalue = PyVMValue.pyint(result)
        self.stack.append(pyvalue)

    def imul(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        result = val1.value * val2.value
        pyvalue = PyVMValue.pyint(result)
        self.stack.append(pyvalue)

    def idiv(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        result = val2.value // val1.value
        pyvalue = PyVMValue.pyint(result)
        self.stack.append(pyvalue)

    def irem(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        pyvalue = PyVMValue.pyint(val2.value % val1.value)
        self.stack.append(pyvalue)

    def ior(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        pyvalue = PyVMValue.pyint(val1.value | val2.value)
        self.stack.append(pyvalue)

    def ineg(self):
        val1 = self.stack.pop()
        pyvalue = PyVMValue.pyint(-1 * val1.value)
        self.stack.append(pyvalue)

    def iand(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        pyvalue = PyVMValue.pyint(val1.value & val2.value)
        self.stack.append(pyvalue)

    def iconst(self, value) -> None:
        pyvalue = PyVMValue.pyint(value)
        self.stack.append(pyvalue)

    def pop(self) -> PyVMValue: 
        return self.stack.pop()

    def push(self, pyvalue: PyVMValue) -> None:
        self.stack.append(pyvalue)

    def dadd(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        pyvalue = PyVMValue.pydouble(val2.value + val1.value)
        self.stack.append(pyvalue)

    def dsub(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        pyvalue = PyVMValue.pydouble(val2.value - val1.value)
        self.stack.append(pyvalue)

    def dmul(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        pyvalue = PyVMValue.pydouble(val1.value * val2.value)
        self.stack.append(pyvalue)

    def ddiv(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        pyvalue = PyVMValue.pydouble(val2.value // val1.value)
        self.stack.append(pyvalue)

    def dneg(self) -> None:
        val1 = self.stack.pop()
        pyvalue = PyVMValue.pydouble(-1 * val1.value)
        self.stack.append(pyvalue)

    def drem(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        pyvalue = PyVMValue.pydouble(val2.value % val1.value)
        self.stack.append(pyvalue)

    def dconst(self, value) -> None:
        pyvalue = PyVMValue.pydouble(value)
        self.stack.append(pyvalue)

    def dup(self) -> None:
        val = self.stack.pop()
        self.stack.append(val)
        self.stack.append(val)

    def dup2(self) -> None:
        #FIXME
        val = self.stack.pop()
        self.stack.append(val)
        self.stack.append(val)

    def __str__(self) -> str:
        return "IntrptEvalStack(stack={})".format(self.stack)

    def __repr__(self) -> str:
        return self.__str__()

