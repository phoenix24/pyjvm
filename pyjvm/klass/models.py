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
    def __init__(self, klass, flags, name, nameIdx, type, descIdx):
        super().__init__(klass, flags, nameIdx, descIdx)
        self.name = name
        self.type = type

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "PyField(klass={}, name={}, nameIdx={}, type={}, flags={}, descIdx={})".format(
            self.klass, self.name, self.nameidx, self.type, self.flags, self.descidx
        )

    def __eq__(self, other):
        return isinstance(other, PyField)\
           and self.klass == other.klass \
           and self.flags == other.flags \
           and self.type == other.type \
           and self.name == other.name \
           and self.nameidx == other.nameidx \
           and self.descidx == other.descidx


class PyMethod(PyBase):
    def __init__(self, klass, flags, nameIdx, name, descIdx, desc):
        super().__init__(klass, flags, nameIdx, descIdx)
        self.bytecode = []
        self.signature = desc
        self.name_type = "{}:{}".format(name, desc)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "PyMethod(klass={}, name_type={}, nameIdx={}, flags={}, descidx={}, desc={}, bytecode={})".format(
            self.klass, self.name_type, self.nameidx, self.flags, self.descidx, self.signature, self.bytecode
        )

    def __eq__(self, other):
        return isinstance(other, PyMethod) \
            and self.klass == other.klass \
            and self.flags == other.flags \
            and self.descidx == other.descidx \
            and self.nameidx == other.nameidx \
            and self.name_type == other.name_type


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
