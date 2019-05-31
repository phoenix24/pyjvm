from enum import Enum
from typing import Dict, List, Set, TypeVar

PyVMNumber = TypeVar('PyVMNumber', int, float)
PyObjFields = TypeVar('PyObjFields', List['PyVMValue'], List[None])


class PyVMType(Enum):
    Z = 0
    B = 1
    S = 2
    C = 3
    I = 5
    J = 6
    F = 7
    D = 8
    A = 9


class PyVMValue(object):
    def __init__(self, type: PyVMType, value: PyVMNumber):
        self.type = type
        self.value = value
    
    def copy(self, value=None, type=None):
        type = type or self.type
        value = value if (value is not None) else self.value
        return PyVMValue(type, value)

    def clone(self):
        return PyVMValue(self.type, self.value)

    @staticmethod
    def pyref(value: int):
        return PyVMValue(PyVMType.A, value)

    @staticmethod
    def pyint(value: int):
        return PyVMValue(PyVMType.I, value)

    @staticmethod
    def pylong(value: int):
        return PyVMValue(PyVMType.J, value)

    @staticmethod
    def pyfloat(value: float):
        return PyVMValue(PyVMType.F, value)

    @staticmethod
    def pydouble(value: float):
        return PyVMValue(PyVMType.D, value)

    def __type__(self, other: 'PyVMValue'):
        return isinstance(other, PyVMValue) \
            and self.type == other.type

    def __or__(self, other: 'PyVMValue') -> 'PyVMValue':
        value = self.value | other.value
        return self.copy(value=value)

    def __and__(self, other: 'PyVMValue') -> 'PyVMValue':
        value = self.value & other.value
        return self.copy(value=value)

    def __neg__(self) -> 'PyVMValue':
        value = -1 * self.value
        return self.copy(value=value)

    def __lshift__(self, val) -> 'PyVMValue':
        value = self.value << val
        return self.copy(value=value)

    def __rshift__(self, val) -> 'PyVMValue':
        value = self.value >> val
        return self.copy(value=value)

    def __add__(self, other: 'PyVMValue') -> 'PyVMValue':
        value = self.value + other.value
        return self.copy(value=value)

    def __sub__(self, other: 'PyVMValue') -> 'PyVMValue':
        value = self.value - other.value
        return self.copy(value=value)

    def __mul__(self, other: 'PyVMValue') -> 'PyVMValue':
        value = self.value * other.value
        return self.copy(value=value)

    def __mod__(self, other: 'PyVMValue') -> 'PyVMValue':
        value = self.value % other.value
        return self.copy(value=value)

    def __truediv__(self, other: 'PyVMValue') -> 'PyVMValue':
        value = self.value / other.value
        return PyVMValue(PyVMType.F, value)

    def __floordiv__(self, other: 'PyVMValue') -> 'PyVMValue':
        value = self.value // other.value
        return self.copy(value=value)

    def __eq__(self, other: 'PyVMValue') -> bool:
        return self.__type__(other) \
            and self.value == other.value

    def __ne__(self, other: 'PyVMValue'):
        return not self.__eq__(other)

    def __lt__(self, other: 'PyVMValue'):
        return self.__type__(other) \
            and self.value < other.value

    def __le__(self, other: 'PyVMValue'):
        return self.__type__(other) \
            and self.value <= other.value

    def __gt__(self, other: 'PyVMValue'):
        return self.__type__(other) \
            and self.value > other.value

    def __ge__(self, other: 'PyVMValue'):
        return self.__type__(other) \
            and self.value >= other.value

    def __str__(self):
        return "PyVMValue(type={}, value={})".format(self.type, self.value)

    def __repr__(self):
        return self.__str__()


class PyVMKonst(object):
    ACC_PUBLIC = 0x0001       # Declared public; may be accessed from outside its package.
    ACC_PRIVATE = 0x0002      # Declared private; usable only within the defining class.
    ACC_PROTECTED = 0x0004    # Declared protected; may be accessed within subclasses.
    ACC_STATIC = 0x0008       # Declared static
    ACC_FINAL = 0x0010        # Declared final; no subclasses allowed.
    ACC_SUPER = 0x0020        # (Class) Treat superclass methods specially when invoked by the invokespecial instruction.
    ACC_VOLATILE = 0x0040     # (Field) Declared volatile; cannot be cached.
    ACC_TRANSIENT = 0x0080    # (Field) Declared transient; not written or read by a persistent object manager.
    ACC_INTERFACE = 0x0200    # (Class) Is an interface, not a class.
    ACC_ABSTRACT = 0x0400     # (Class) Declared abstract; must not be instantiated.
    ACC_SYNTHETIC = 0x1000    # Declared synthetic; not present in the source code.
    ACC_ANNOTATION = 0x2000   # Declared as an annotation type.
    ACC_ENUM = 0x4000         # Declared as an enum type.

    # method only constants
    ACC_SYNCHRONIZED = 0x0020 # (Method) Declared synchronized; invocation is wrapped by a monitor use.
    ACC_BRIDGE = 0x0040       # (Method) A bridge, generated by the compiler.
    ACC_VARARGS = 0x0080      # (Method) Declared with variable number of arguments.
    ACC_NATIVE = 0x0100       # (Method) Declared native; implemented in a language other than Java.
    ACC_ABSTRACT_M = 0x0400   # (Method) Declared abstract; no implementation is provided.
    ACC_STRICT = 0x0800       # (Method) Declared strictfp; floating-point mode is FP-strict.


class PyVMKlass(object):
    def __init__(self, klass: str, super: str):
        self.name: str = klass
        self.super: str = super

        self.items = {}
        self.klassByIndex: Dict[int, str] = {}

        self.fields: Dict[str, PyVMField] = {}
        self.fieldsByIndex: Dict[int, str] = {}
        self.orderedFields: List[PyVMField] = []
        self.staticFieldByName: Dict[str, PyVMValue] = {}

        self.methods: Dict[str, PyVMMethod] = {}
        self.methodsByIndex: Dict[int, str] = {}

    def add_defined_method(self, method: 'PyVMMethod') -> None:
        self.methods.update({method.name_type: method})

    def add_defined_field(self, field) -> None:
        self.fields.update({field.name: field})

    def add_field(self, field: 'PyVMField') -> None:
        self.fields.update({field.name: field})
        if field.flags & PyVMKonst.ACC_STATIC:
            self.staticFieldByName.update({field.name: None})
        else:
            self.orderedFields.append(field)

    def get_klass_by_idx(self, index) -> str:
        return self.klassByIndex[index]

    def add_klass_ref(self, index: int, name: str) -> None:
        self.klassByIndex.update({index: name})

    def add_field_ref(self, index: int, name: str) -> None:
        self.fieldsByIndex.update(({index: name}))

    def add_method_ref(self, index: int, name: str) -> None:
        self.methodsByIndex.update({index: name})

    def get_fields(self) -> List[str]:
        return list(self.fields.keys())

    def get_fields_count(self) -> int:
        return len(self.fields.keys())

    def get_field_by_idx(self, index) -> str:
        return self.fieldsByIndex[index]

    def get_field_offset(self, field):
        return 0 #TODO

    def get_static_field(self, field: 'PyVMField') -> PyVMValue:
        return self.staticFieldByName[field.name]

    def set_static_field(self, name: str, value: PyVMValue) -> None:
        self.staticFieldByName.update({name: value})

    def get_method(self, name: str) -> 'PyVMMethod':
        return self.methods[name]

    def get_methods(self) -> List[str]:
        return list(self.methods.keys())

    def get_method_by_idx(self, index: int) -> str:
        return self.methodsByIndex[index]

    def __eq__(self, other):
        return isinstance(other, PyVMKlass) \
           and self.name == other.name \
           and self.super == other.super \
           and self.items == other.items \
           and self.klassByIndex == other.klassByIndex \
           and self.fields == other.fields \
           and self.fieldsByIndex == other.fieldsByIndex \
           and self.orderedFields == other.orderedFields \
           and self.staticFieldByName == other.staticFieldByName \
           and self.methods == other.methods \
           and self.methodsByIndex == other.methodsByIndex

    def __str__(self):
        return "PyVMKlass(name={}, methods={}, methodsIdx={}, fields={}, staticfields={})".format(
            self.name, len(self.methods), len(self.methodsByIndex), len(self.fields), len(self.staticFieldByName)
        )

    def __repr__(self):
        return self.__str__()


class PyVMField(object):
    def __init__(self, klass: PyVMKlass, name: str, type: PyVMType, flags: int):
        self.name = name
        self.type = type
        self.klass = klass
        self.flags = flags

    def __str__(self):
        return "PyVMField(name={}, type={}, klass={}, flags={}".format(
            self.name, self.type, self.klass, self.flags
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, PyVMField) \
           and self.name == other.name \
           and self.type == other.type \
           and self.klass == other.klass \
           and self.flags == other.flags


class PyVMMethod(object):
    def __init__(self, klass: PyVMKlass, signature, name_type: str, bytecode, flags: int):
        self.args = -1
        self.klass = klass
        self.flags = flags
        self.bytecode = bytecode
        self.signature = signature
        self.name_type = name_type

    def is_static(self) -> bool:
        return not not (self.flags & PyVMKonst.ACC_STATIC)

    @property
    def num_params(self) -> int:
        if self.args > -1:
            return self.args

        index, self.args = 0, 0
        while index < len(self.signature):
            char = self.signature[index]
            if char in ('Z', 'B', 'S', 'C', 'I', 'J', 'F', 'D'):
                self.args += 1
            elif char == ')':
                return self.args
            elif char == 'L':
                while self.signature[index] != ';':
                    index += 1
            index += 1

        return self.args

    def __str__(self):
        return "PyVMMethod(klass={}, name_type={}, flags={}, args={})".format(
            self.klass.name, self.name_type, self.flags, self.args
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: 'PyVMMethod'):
        return isinstance(other, PyVMMethod) \
           and self.klass == other.klass \
           and self.flags == other.flags \
           and self.bytecode == other.bytecode \
           and self.signature == other.signature \
           and self.name_type == other.name_type


class PyVMObject(object):

    def __init__(self, id: int, _klazz: PyVMKlass):
        self.idx: int = id
        self.klass: PyVMKlass = _klazz
        self.fields: PyObjFields = [None] * _klazz.get_fields_count()

    @classmethod
    def new(cls, klazz: PyVMKlass, _id: int):
        object = PyVMObject(_id, klazz)
        return object

    def get_field(self, field: PyVMField):
        offset = self.klass.get_field_offset(field)
        return self.fields[offset]

    def set_field(self, field: PyVMField, val: PyVMValue) -> None:
        offset = self.klass.get_field_offset(field)
        self.fields[offset] = val

    def __eq__(self, other):
        return isinstance(other, PyVMObject) \
           and self.idx == other.idx \
           and self.klass == other.klass \
           and self.fields == other.fields

