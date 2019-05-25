from .models import PyVMValue


class IntrptEvalStack(object):
    def __init__(self):
        self.stack = []

    def aconst_null(self):
        pass

    def iadd(self):
        val1 = self.stack.pop()
        val2 = self.stack.pop()
        result = val1.value + val2.value
        pyvalue = PyVMValue.pyint(result)
        self.stack.append(pyvalue)

    def iconst(self, value):
        pyvalue = PyVMValue.pyint(value)
        self.stack.append(pyvalue)

    def pop(self) -> PyVMValue: 
        return self.stack.pop()

    def push(self, pyvalue: PyVMValue): 
        self.stack.append(pyvalue)

    def __str__(self):
        return "IntrptEvalStack(stack={})".format(self.stack)

    def __repr__(self):
        return self.__str__()

