#!//usr/bin/env python

import os, sys
from pyrt.models import PyRtKlass, PyRtMethod, PyRtField, PyVMType
from pyutils import toint, tostring, usage
from pyexception import PyKlassNotFoundException, PyTypeNotFoundException, PyIllegalArgumentException
from pyklass.models import PyRef, PyAttr, PyMethod, PyField, PyKPEntry, PyKPType


class PyReader(object):
    @staticmethod
    def read(file):
        bytes = []
        with open(file, 'rb') as bfile:
            byte = bfile.read(1)
            while byte:
                bytes.append(byte)
                byte = bfile.read(1)
        return bytes


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
        self.__init()
        self.__header()
        self.__constant_pool()
        self.__basic_type_info()
        self.__fields()
        self.__methods()
        return self

    def build(self):
        klass = PyRtKlass(self.klass, self.super)

        for field in self.fields:
            fd = PyRtField(klass, field.name, field.type, field.flags)
            klass.add_field(fd)
            klass.add_defined_field(fd)

        for mt in self.methods:
            mt = PyRtMethod(self.klass, mt.signature, mt.name_type, mt.flags, mt.bytecode)
            klass.add_defined_method(mt)

        for entry in self.pool_items:
            if entry.type == "CLASS":
                klassIdx = entry.ref1.index
                klassName = self.__resolve(klassIdx)
                klass.add_klass_ref(entry.index, klassName)

            elif entry.type == "FIELDREF":
                klassIdx = entry.ref1.index
                klassName = self.__resolve(klassIdx)
                nameTypeIdx = entry.ref2.index
                nameType = self.__resolve(nameTypeIdx)
                klass.add_field_ref(entry.index, "{}.{}".format(klassName, nameType))

            elif entry.type == "METHODREF":
                klassIdx = entry.ref1.index
                klassName = self.__resolve(klassIdx)
                nameTypeIdx = entry.ref2.index
                nameType = self.__resolve(nameTypeIdx)
                klass.add_method_ref(entry.index, "{}.{}".format(klassName, nameType))

        print("fields: ", len(self.fields))
        print("methods: ", len(self.methods))
        print("poolitems: ", len(self.pool_items))
        return klass

    def __init(self):
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

    def __kptable(self, kptype):
        self.kptable[kptype.val] = kptype

    def __header(self):
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

    def __fields(self):
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

    def __methods(self):
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

    def __constant_pool(self):
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

    def __basic_type_info(self):
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


class PyInterp(object):
    def __init__(self, repo):
        self.repo = repo

    def execute(self, method):
        pass


if __name__ == '__main__':
    args = sys.argv
    if len(args) >= 2 and not args[1].endswith(".class"):
        usage()
        
    kfile = args[1]
    bytes = PyReader.read(kfile)
    parser = PyParser(bytes).parse()
    pyklass = parser.build()
    print("execution complete")

