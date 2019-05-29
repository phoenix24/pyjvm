from .models import PyVMValue, PyVMType
from typing import List, Dict, Sequence, Mapping


class IntrptEvalStack(object):
    def __init__(self, stack=None):
        self.stack: List[PyVMValue] = stack or []

    def aconst_null(self):
        self.stack.append(PyVMValue(PyVMType.A, 0))

    def iadd(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val1 + val2)

    def isub(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val2 - val1)

    def imul(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val1 * val2)

    def idiv(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val2 // val1)

    def irem(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val2 % val1)

    def ior(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val1 | val2)

    def ineg(self):
        val1 = self.stack.pop()
        self.stack.append(-val1)

    def iand(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val1 & val2)

    def iconst(self, value: int) -> None:
        pyvalue = PyVMValue.pyint(value)
        self.stack.append(pyvalue)

    def pop(self) -> PyVMValue: 
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def push(self, pyvalue: PyVMValue) -> None:
        self.stack.append(pyvalue)

    def dadd(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val1 + val2)

    def dsub(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val2 - val1)

    def dmul(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val2 * val1)

    def ddiv(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val2 // val1)

    def dneg(self) -> None:
        val1 = self.stack.pop()
        self.stack.append(-val1)

    def drem(self) -> None:
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val2 % val1)

    def dconst(self, value: float) -> None:
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

    def dup_x1(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val1.clone())
        self.stack.append(val2)
        self.stack.append(val1)

    def swap(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        self.stack.append(val1)
        self.stack.append(val2)

    def size(self):
        return len(self.stack)

    def __i2t(self, type: PyVMType):
        val = self.stack.pop()
        val = PyVMValue(type, val.value)
        self.stack.append(val)

    def i2b(self):
        self.__i2t(PyVMType.B)

    def i2d(self):
        self.__i2t(PyVMType.D)

    def i2c(self):
        self.__i2t(PyVMType.C)

    def i2f(self):
        self.__i2t(PyVMType.F)

    def i2l(self):
        self.__i2t(PyVMType.J)

    def i2s(self):
        self.__i2t(PyVMType.S)

    def __str__(self) -> str:
        return "IntrptEvalStack(stack={})".format(self.stack)

    def __repr__(self) -> str:
        return self.__str__()
