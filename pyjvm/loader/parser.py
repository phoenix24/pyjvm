
from pyjvm.rt.models import PyVMKlass, PyVMMethod, PyVMField, PyVMType, PyVMKonst
from pyjvm.klass.models import PyRef, PyAttr, PyMethod, PyField, PyKPEntry, PyKPType
from pyjvm.utils.converter import toint, tostring
from pyjvm.exception import PyKlassNotFoundException, PyTypeNotFoundException, PyIllegalArgumentException


class PyParser(object):
    def __init__(self, bytes):
        self.bytes = bytes
        self.offset = 0

        self.major = None
        self.minor = None
        
        self.pool_items = []
        self.pool_count = None
        
        self.kptable = {}
        self.kptypes = []

        self.flags = None
        self.fields = []
        self.methods = []
        self.kentrys = []
        self.interfaces = []

        self.klass = None
        self.klassIdx = None

        self.super = None
        self.superIdx = None

    def parse(self):
        self._init()
        self._header()
        self._constant_pool()
        self._basic_type_info()
        self._fields()
        self._methods()
        return self

    def build(self) -> PyVMKlass:
        klass = PyVMKlass(self.klass, self.super)

        for field in self.fields:
            fd = PyVMField(klass, field.name, field.type, field.flags)
            klass.add_field(fd)
            klass.add_defined_field(fd)

        for md in self.methods:
            mt = PyVMMethod(klass, md.signature, md.name_type, md.bytecode, md.flags)
            klass.add_defined_method(mt)

        for entry in self.pool_items:
            pytype = entry.type.type
            if pytype == "CLASS":
                klassIdx = entry.ref1.index
                klassName = self.__resolve(klassIdx)
                klass.add_klass_ref(entry.index, klassName)

            elif pytype == "FIELDREF":
                klassIdx = entry.ref1.index
                klassName = self.__resolve(klassIdx)
                nameTypeIdx = entry.ref2.index
                nameType = self.__resolve(nameTypeIdx)
                klass.add_field_ref(entry.index, "{}.{}".format(klassName, nameType))

            elif pytype == "METHODREF":
                klassIdx = entry.ref1.index
                klassName = self.__resolve(klassIdx)
                nameTypeIdx = entry.ref2.index
                nameType = self.__resolve(nameTypeIdx)
                klass.add_method_ref(entry.index, "{}.{}".format(klassName, nameType))
        return klass

    def _init(self):
        self.__kptable(PyKPType(1, "UTF8"))
        self.__kptable(PyKPType(3, "INTEGER"))
        self.__kptable(PyKPType(4, "FLOAT"))
        self.__kptable(PyKPType(5, "LONG"))
        self.__kptable(PyKPType(6, "DOUBLE"))
        self.__kptable(PyKPType(7, "CLASS"))
        self.__kptable(PyKPType(8, "STRING"))
        self.__kptable(PyKPType(9, "FIELDREF", "."))
        self.__kptable(PyKPType(10, "METHODREF", "."))
        self.__kptable(PyKPType(11, "INTERFACE_METHODREF"))
        self.__kptable(PyKPType(12, "NAMEANDTYPE", ":"))
        self.__kptable(PyKPType(15, "METHODHANDLE"))
        self.__kptable(PyKPType(16, "METHODTYPE"))
        self.__kptable(PyKPType(18, "INVOKEDYNAMIC"))

    def __kptable(self, kptype: PyKPType) -> None:
        self.kptable[kptype.val] = kptype

    def _header(self):
        bytes = self.bytes[:4]
        header = [0xca, 0xfe, 0xba, 0xbe]
        for actual, expected in zip(bytes, header):
            actual = toint(actual)
            if actual != expected: 
                raise Exception("invalid header. expected:%s found:%s" % (expected, actual))

        self.minor = (toint(self.bytes[4]) << 8) + toint(self.bytes[5])
        self.major = (toint(self.bytes[6]) << 8) + toint(self.bytes[7])
        self.pool_count = toint(self.bytes[8]) + toint(self.bytes[9])
        self.pool_items = []
        self.offset += 10

    def _fields(self):
        oft = self.offset
        cnt = (toint(self.bytes[oft + 0]) << 8) + toint(self.bytes[oft + 1])
        self.offset += 2
        oft = self.offset

        for index in range(cnt):
            flags   = (toint(self.bytes[oft + 0]) << 8) + toint(self.bytes[oft + 1])
            nameidx = (toint(self.bytes[oft + 2]) << 8) + toint(self.bytes[oft + 3])
            descidx = (toint(self.bytes[oft + 4]) << 8) + toint(self.bytes[oft + 5])
            attrcnt = (toint(self.bytes[oft + 6]) << 8) + toint(self.bytes[oft + 7])

            desc = self.__resolve(descidx)
            pytype = PyVMType['A'] if desc.startswith("L") else PyVMType[desc]
            pyfield = PyField(
                self.klass, flags, self.__resolve(nameidx), nameidx, pytype, descidx
            )
            self.offset += 8

            for attrix in range(attrcnt):
               attribute = self.__parse_attribute(pyfield)
               pyfield.attrs.append(attribute)
            self.fields.append(pyfield)

    def _methods(self):
        oft = self.offset
        cnt = (toint(self.bytes[oft + 0]) << 8) + toint(self.bytes[oft + 1])
        self.offset += 2

        for index in range(cnt):
            oft = self.offset
            flags   = (toint(self.bytes[oft + 0]) << 8) + toint(self.bytes[oft + 1])
            nameIdx = (toint(self.bytes[oft + 2]) << 8) + toint(self.bytes[oft + 3])
            descIdx = (toint(self.bytes[oft + 4]) << 8) + toint(self.bytes[oft + 5])
            attrcnt = (toint(self.bytes[oft + 6]) << 8) + toint(self.bytes[oft + 7])
            pymethod = PyMethod(
                self.klass, flags, nameIdx, self.__resolve(nameIdx), descIdx, self.__resolve(descIdx)
            )
            self.offset += 8

            for attrix in range(attrcnt):
               attribute = self.__parse_attribute(pymethod)
               pymethod.attrs.append(attribute)
            self.methods.append(pymethod)

    def _constant_pool(self):
        for index in range(1, self.pool_count):
            entry = toint(self.bytes[self.offset]) & 0xff
            kptype = self.kptable[entry]
            self.offset += 1

            if kptype.type == "UTF8":
                length = (toint(self.bytes[self.offset]) << 8) + toint(self.bytes[self.offset + 1])
                bytestr = tostring(self.bytes[self.offset + 2: self.offset + 2 + length])
                self.offset += 2 + length
                self.pool_items.append(PyKPEntry(index, kptype, bytestr))

            elif kptype.type == "INTEGER":
                oft = self.offset
                val = (toint(self.bytes[oft + 0]) << 24) \
                    + (toint(self.bytes[oft + 1]) << 16) \
                    + (toint(self.bytes[oft + 2]) << 8) \
                    + (toint(self.bytes[oft + 3]))
                self.offset += 4
                self.pool_items.append(PyKPEntry(index, kptype, val))

            elif kptype.type == "FLOAT":
                oft = self.offset
                val = (toint(self.bytes[oft + 0]) << 24) \
                    + (toint(self.bytes[oft + 1]) << 16) \
                    + (toint(self.bytes[oft + 2]) << 8) \
                    + (toint(self.bytes[oft + 3]))
                # todo: change to float.
                self.offset += 4
                self.pool_items.append(PyKPEntry(index, kptype, val))

            elif kptype.type == "LONG":
                oft = self.offset
                val1 = (toint(self.bytes[oft + 0]) << 24) \
                     + (toint(self.bytes[oft + 1]) << 16) \
                     + (toint(self.bytes[oft + 2]) << 8) \
                     + (toint(self.bytes[oft + 3]))
                val2 = (toint(self.bytes[oft + 4]) << 24) \
                     + (toint(self.bytes[oft + 5]) << 16) \
                     + (toint(self.bytes[oft + 6]) << 8) \
                     + (toint(self.bytes[oft + 7]))
                val  = (val1 << 32) + val2
                # todo: change to long.
                self.offset += 8
                self.pool_items.append(PyKPEntry(index, kptype, val))

            elif kptype.type == "DOUBLE":
                oft = self.offset
                val1 = (toint(self.bytes[oft + 0]) << 24) \
                     + (toint(self.bytes[oft + 1]) << 16) \
                     + (toint(self.bytes[oft + 2]) << 8) \
                     + (toint(self.bytes[oft + 3]))
                val2 = (toint(self.bytes[oft + 4]) << 24) \
                     + (toint(self.bytes[oft + 5]) << 16) \
                     + (toint(self.bytes[oft + 6]) << 8) \
                     + (toint(self.bytes[oft + 7]))
                val  = (val1 << 32) + val2
                # todo: change to long.
                self.offset += 8
                self.pool_items.append(PyKPEntry(index, kptype, val))

            elif kptype.type == "CLASS":
                klassRef = (toint(self.bytes[self.offset]) << 8) + toint(self.bytes[self.offset + 1])
                self.offset += 2
                self.pool_items.append(
                    PyKPEntry(index, kptype, ref1=PyRef(klassRef))
                )

            elif kptype.type == "STRING":
                strRef = (toint(self.bytes[self.offset]) << 8) + toint(self.bytes[self.offset + 1])
                self.offset += 2
                self.pool_items.append(
                    PyKPEntry(index, kptype, ref1=PyRef(strRef))
                )

            elif kptype.type == "NAMEANDTYPE":
                nameRef = (toint(self.bytes[self.offset + 0]) << 8) + toint(self.bytes[self.offset + 1])
                typeRef = (toint(self.bytes[self.offset + 2]) << 8) + toint(self.bytes[self.offset + 3])
                self.offset += 4
                self.pool_items.append(
                    PyKPEntry(index, kptype, ref1=PyRef(nameRef), ref2=PyRef(typeRef))
                )

            elif kptype.type == "FIELDREF" \
              or kptype.type == "METHODREF" \
              or kptype.type == "INTERFACE_METHODREF":
                kpIndex = (toint(self.bytes[self.offset + 0]) << 8) + toint(self.bytes[self.offset + 1])
                ntIndex = (toint(self.bytes[self.offset + 2]) << 8) + toint(self.bytes[self.offset + 3])
                self.offset += 4
                self.pool_items.append(
                    PyKPEntry(index, kptype, ref1=PyRef(kpIndex), ref2=PyRef(ntIndex))
                )

            else:
                raise PyKlassNotFoundException("class not found exception")

    def _basic_type_info(self):
        oft = self.offset
        self.flags = (toint(self.bytes[oft + 0]) << 8) + toint(self.bytes[oft + 1])

        self.klassIdx = (toint(self.bytes[oft + 2]) << 8) + toint(self.bytes[oft + 3])
        self.klass = self.__resolve(self.klassIdx)

        self.superIdx = (toint(self.bytes[oft + 4]) << 8) + toint(self.bytes[oft + 5])
        self.super = self.__resolve(self.superIdx)

        cnt = (toint(self.bytes[oft + 6]) << 8) + toint(self.bytes[oft + 7])
        calc = lambda x: (toint(self.bytes[oft + x + 8]) << 8) + toint(self.bytes[oft + x + 9])
        self.interfaces = [calc(index) for index in range(cnt)]
        self.offset += (4 * 2) + (cnt * 2)

    def __parse_attribute(self, item):
        oft = self.offset
        nameIdx = (toint(self.bytes[oft + 0]) << 8) + toint(self.bytes[oft + 1])
        attrLen = (toint(self.bytes[oft + 2]) << 24) + \
                  (toint(self.bytes[oft + 3]) << 16) + \
                  (toint(self.bytes[oft + 4]) << 8)  + \
                  (toint(self.bytes[oft + 5]) << 0)
        endIndex = self.offset + attrLen + 6

        self.offset += 6
        entry = self.pool_items[nameIdx - 1]

        if entry.string == "ConstantValue":
            if isinstance(entry, PyMethod):
                desc = "{}:{}".format(self.__resolve(item.nameidx), self.__resolve(item.descidx))
                raise PyIllegalArgumentException("Method {} cannot be constant".format(desc))
            # TODO
            self.offset += 2

        elif entry.string == "Code":
            # method expected here, it's code after all :D.
            if isinstance(item, PyField):
                desc = "{}:{}".format(self.__resolve(item.nameidx), self.__resolve(item.descidx))
                raise PyIllegalArgumentException("Field {} cannot contain code".format(desc))

            self.offset += 4
            oft = self.offset
            codeLen = (toint(self.bytes[oft + 0]) << 24) + \
                      (toint(self.bytes[oft + 1]) << 16) + \
                      (toint(self.bytes[oft + 2]) << 8)  + \
                      (toint(self.bytes[oft + 3]) << 0)
            self.offset += 4
            item.bytecode = self.bytes[self.offset: self.offset + codeLen]

        elif entry.string == "Exceptions":
            print("encountered exception handler in bytecode, skipping!")

        else:
            raise PyIllegalArgumentException("unhandled attribute type", entry)

        self.offset = endIndex
        return PyAttr(nameIdx)

    def __resolve(self, index):
        entry = self.pool_items[index - 1]
        entry_type = entry.type.type

        if entry_type == "UTF8":
            return entry.string

        elif entry_type == "INTEGER":
            return str(entry.number)

        elif entry_type == "FLOAT":
            return str(entry.number)

        elif entry_type == "LONG":
            return str(entry.number)

        elif entry_type == "DOUBLE":
            return str(entry.number)

        elif entry_type in ("CLASS", "STRING"):
            other = self.pool_items[entry.ref1.index - 1]
            return other.string

        elif entry_type in ("FIELDREF", "METHODREF", "INTERFACE_METHODREF", "NAMEANDTYPE"):
            left = entry.ref1.index
            right = entry.ref2.index
            return "%s%s%s" % (self.__resolve(left), entry.type.sep, self.__resolve(right))

        else:
            raise PyTypeNotFoundException("impossible constant type", entry)
