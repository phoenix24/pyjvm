class PyBase(object):
    def __init__(self, flags, nameidx, descidx, attrcnt):
        self.flags = flags
        self.nameidx = nameidx
        self.descidx = descidx
        self.attrcnt = attrcnt


class PyField(PyBase):
    def __init__(self, flags, nameidx, descidx, attrcnt):
        super().__init__(flags, nameidx, descidx, attrcnt)
        self.name = "" # todo
        self.jvmtype = "" # todo


class PyMethod(PyBase):
    def __init__(self, flags, nameidx, descidx, attrcnt):
        super().__init__(flags, nameidx, descidx, attrcnt)
        self.bytes = []
        self.signature = "" # todo
        self.name_and_type = "" # todo


class PyKPEntry(object):
    def __init__(self, index, type, number=None, string=None, ref1=None, ref2=None):
        self.ref1 = ref1
        self.ref2 = ref2
        self.type = type
        self.index = index
        self.number = number
        self.string = string or (str(number) if number else None)


class PyKlass(object):
    def __init__(self, ):
        #class
        #super-classes
        #methods
        #fields
        #static fields
        pass
