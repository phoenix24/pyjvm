from typing import Dict, List
from pyjvm.rt.models import PyVMField, PyVMKlass, PyVMObject


class SimpleHeap(object):

    def __init__(self):
        self.counter = 0
        self.heap: Dict[int, PyVMObject] = {}

    def gc(self) -> None:
        print(">>> woops! pyjvm no gc")

    def find(self, objectid) -> PyVMObject:
        return self.heap.get(objectid)

    def allocate(self, klazz: PyVMKlass) -> int:
        self.counter += 1
        object = PyVMObject.new(klazz, self.counter)
        self.heap.update({object.idx: object})
        return object.idx
