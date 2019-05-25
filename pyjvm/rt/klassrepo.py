from pyjvm.exception import PyVMIllegalStateException

class SharedRepo(object):
    def __init__(self):
        self.klass_cache = {}
        self.field_cache = {}
        self.method_cache = {}

    def add(self, klass):
        self.klass_cache.update({klass.name: klass})
        for name, field in klass.fields.items():
            name = "{}.{}.{}".format(field.klass.name, field.name, field.type)
            self.field_cache.update({name: field})

        for name, method in klass.methods.items():
            name = "{}.{}".format(method.klass.name, method.name_type)
            self.method_cache.update({name: method})

    def lookupKlass(self, name, nameIdx):
        pass

    def lookupField(self, name, nameIdx):
        pass

    def lookupMethodExact(self, name: str, nameIdx: int):
        klass = self.klass_cache[name]
        mname = klass.get_method_by_idx(nameIdx)
        method = self.method_cache.get(mname)
        if not method:
            message = "method of signature {} from index {} not found on class {}".format(mname, nameIdx, klass)
            raise PyVMIllegalStateException(message)
        return method

    def lookupMethodVirtual(self, name, nameIdx):
        pass