class PyRef(object):
    def __init__(self, index):
        self.index = index

    def __str__(self):
        return str(self.index)


class PyAttr(object):
    def __init__(self, nameIdx, name="tmp"):
        self.name = name
        self.nameIdx = nameIdx


class PyBase(object):
    def __init__(self, klass, flags, nameIdx, descIdx):
        self.flags = flags
        self.klass = klass
        self.attrs = []
        self.nameidx = nameIdx
        self.descidx = descIdx


class PyField(PyBase):
    def __init__(self, klass, flags, name, nameIdx, pytype, descIdx):
        super().__init__(klass, flags, nameIdx, descIdx)
        self.name = name
        self.type = pytype

    def __str__(self):
        return "PyField(klass={}, field={})".format(self.klass, self.name)


class PyMethod(PyBase):
    def __init__(self, klass, flags, nameIdx, name, descIdx, desc):
        super().__init__(klass, flags, nameIdx, descIdx)
        self.bytecode = []
        self.signature = desc
        self.name_type = "{}:{}".format(name, desc)

    def __str__(self):
        return "PyMethod(klass={}, method={})".format(self.klass, self.name_type)


class PyKPType(object):
    def __init__(self, val, type, sep = ""):
        self.val = val
        self.sep = sep
        self.type = type

    def __str__(self):
        return "PyKPType(val={}, type={}, sep={})".format(self.val, self.type, self.sep)


class PyKPEntry(object):
    def __init__(self, index, type, number=None, string=None, ref1=None, ref2=None):
        self.ref1 = ref1
        self.ref2 = ref2
        self.type = type
        self.index = index
        self.number = number
        self.string = string or (str(number) if number else None)

    def __str__(self):
        return "PyKPEntry(index={}, type={}, string={}, number={}, ref1={}, ref2={}".format(
                    self.index, self.type, self.string, self.number, self.ref1, self.ref2
                )
