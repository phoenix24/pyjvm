from typing import Dict, List, TypeVar
from pyjvm.exception import PyVMIllegalStateException
from pyjvm.rt.models import PyVMKlass, PyVMField, PyVMMethod


class SharedRepo(object):

    OBJECT_CLASS = PyVMKlass('java/lang/Object', 'none')

    def __init__(self):
        self.klass_cache: Dict[str, PyVMKlass] = {
            'java/lang/Object': SharedRepo.OBJECT_CLASS
        }
        self.field_cache: Dict[str, PyVMField] = {}
        self.method_cache: Dict[str, PyVMMethod] = {}

    def add(self, klass: PyVMKlass):
        self.klass_cache.update({klass.name: klass})
        for name, field in klass.fields.items():
            name = "{}.{}:{}".format(field.klass.name, field.name, field.type.name)
            self.field_cache.update({name: field})

        for name, method in klass.methods.items():
            name = "{}.{}".format(method.klass.name, method.name_type)
            self.method_cache.update({name: method})

    def lookupKlass(self, name: str, index: int) -> PyVMKlass:
        klazz = self.klass_cache[name]
        other = klazz.get_klass_by_idx(index)
        return self.klass_cache[other]

    def lookupField(self, name: str, index: int) -> PyVMField:
        klazz = self.klass_cache[name]
        field = klazz.get_field_by_idx(index)
        return self.field_cache[field]

    def lookupMethodExact(self, name: str, nameIdx: int) -> PyVMMethod:
        klass = self.klass_cache[name]
        mname = klass.get_method_by_idx(nameIdx)
        method = self.method_cache.get(mname)
        if not method:
            message = "method of signature {} from index {} not found on class {}".format(mname, nameIdx, klass)
            raise PyVMIllegalStateException(message)
        return method

    def lookupMethodVirtual(self, name, nameIdx) -> PyVMMethod:
        pass