#!//usr/bin/env python

import os, sys
from pyutils import toint
from pyexception import KlassNotFoundException
from pyklass.models import PyMethod, PyField, PyKPEntry


def usage():
    helptxt = """ \
    usage:
    $ ./pyjvm.py <filename.class>
    """
    print(helptxt)


class PyKonst(object):
    # todo
    pass


class PyKPType(object):
    def __init__(self, val, type, sep = ""):
        self.val = val
        self.sep = sep
        self.type = type

    def __str__(self):
        return "PyKPType(val={}, type={}, sep={})".format(self.val, self.type, self.sep)


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
        self.pool_count = -1
        
        self.kptable = {}
        self.kptypes = []

        self.klass = None
        self.flags = None
        self.super = None
        self.fields = []
        self.methods = []
        self.kentrys = []
        self.interfaces = []

    def parse(self):
        self.__init()
        self.__header()
        self.__constant_pool()
        self.__basic_type_info()
        self.__fields()
        self.__methods()
        return self.build()

    def build(self):
        # todo
        pass

    def __init(self):
        # initialize kptable.
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
        self.pool_items = [None] * self.pool_count 
        self.offset += 10

    def __fields(self):
        oft = self.offset
        cnt = (toint(self.bytes[oft + 0]) << 8) + toint(self.bytes[oft + 1])
        for index in range(cnt):
            flags = (toint(self.bytes[oft + 2]) << 8) + toint(self.bytes[oft + 3])
            nameidx = (toint(self.bytes[oft + 4]) << 8) + toint(self.bytes[oft + 5])
            descidx = (toint(self.bytes[oft + 6]) << 8) + toint(self.bytes[oft + 7])
            attrcnt = (toint(self.bytes[oft + 8]) << 8) + toint(self.bytes[oft + 9])
            pyfield = PyField(flags, nameidx, descidx, attrcnt)

            #for attrix in range(attrcnt):
            #    pyfield.setAttr(attrix, self.__parse_attribute(pyfield))
            self.fields.append(pyfield)

        self.offset += 2 + (cnt * 8)

    def __methods(self):
        oft = self.offset
        cnt = (toint(self.bytes[oft + 0]) << 8) + toint(self.bytes[oft + 1])
        for index in range(cnt):
            flags = (toint(self.bytes[oft + 2]) << 8) + toint(self.bytes[oft + 3])
            nameidx = (toint(self.bytes[oft + 4]) << 8) + toint(self.bytes[oft + 5])
            descidx = (toint(self.bytes[oft + 6]) << 8) + toint(self.bytes[oft + 7])
            attrcnt = (toint(self.bytes[oft + 8]) << 8) + toint(self.bytes[oft + 9])
            pymethod = PyMethod(flags, nameidx, descidx, attrcnt)

            #for attrix in range(attrcnt):
            #    pymethod.setAttr(attrix, self.__parse_attribute(pymethod))
            self.fields.append(pymethod)

        self.offset += 2 + (cnt * 8)

    def __constant_pool(self):
        print(self.bytes[:10])
        for index, kp in self.kptable.items():
            print(index, kp)

        for index in range(1, self.pool_count):
            entry = toint(self.bytes[self.offset]) & 0xff
            kptag = self.kptable[entry]
            self.offset += 1

            print(len(self.bytes), self.offset, kptag)

            if kptag.type == "UTF8":
                length = (toint(self.bytes[self.offset]) << 8) + toint(self.bytes[self.offset + 1])
                bytestr = self.bytes[self.offset + 2: self.offset + 2 + length]
                self.offset += 2 + length
                # todo: decode byte-array to string
                self.pool_items.append(PyKPEntry(index, kptag, bytestr))

            elif kptag.type == "INTEGER":
                oft = self.offset
                val = (toint(self.bytes[oft + 0]) << 24) \
                    + (toint(self.bytes[oft + 1]) << 16) \
                    + (toint(self.bytes[oft + 2]) << 8) \
                    + (toint(self.bytes[oft + 3]))
                self.offset += 4
                self.pool_items.append(PyKPEntry(index, kptag, val))

            elif kptag.type == "FLOAT":
                oft = self.offset
                val = (toint(self.bytes[oft + 0]) << 24) \
                    + (toint(self.bytes[oft + 1]) << 16) \
                    + (toint(self.bytes[oft + 2]) << 8) \
                    + (toint(self.bytes[oft + 3]))
                # todo: change to float.
                self.offset += 4
                self.pool_items.append(PyKPEntry(index, kptag, val))

            elif kptag.type == "LONG":
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
                self.pool_items.append(PyKPEntry(index, kptag, val))

            elif kptag.type == "DOUBLE":
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
                self.pool_items.append(PyKPEntry(index, kptag, val))

            elif kptag.type == "CLASS":
                klassRef = (toint(self.bytes[self.offset]) << 8) + toint(self.bytes[self.offset + 1])
                self.offset += 2
                self.pool_items.append(PyKPEntry(index, kptag, ref1=klassRef))

            elif kptag.type == "STRING":
                strRef = (toint(self.bytes[self.offset]) << 8) + toint(self.bytes[self.offset + 1])
                self.offset += 2
                self.pool_items.append(PyKPEntry(index, kptag, ref1=strRef))

            elif kptag.type == "NAMEANDTYPE":
                nameRef = (toint(self.bytes[self.offset + 0]) << 8) + toint(self.bytes[self.offset + 1])
                typeRef = (toint(self.bytes[self.offset + 2]) << 8) + toint(self.bytes[self.offset + 3])
                self.offset += 4
                self.pool_items.append(PyKPEntry(index, kptag, ref1=nameRef, ref2=typeRef))

            elif kptag.type == "FIELDREF" \
              or kptag.type == "METHODREF" \
              or kptag.type == "INTERFACE_METHODREF":
                kpIndex = (toint(self.bytes[self.offset + 0]) << 8) + toint(self.bytes[self.offset + 1])
                ntIndex = (toint(self.bytes[self.offset + 2]) << 8) + toint(self.bytes[self.offset + 3])
                self.offset += 4
                self.pool_items.append(PyKPEntry(index, kptag, ref1=kpIndex, ref2=ntIndex))

            else:
                raise KlassNotFoundException("class not found exception")

    def __basic_type_info(self):
        oft = self.offset
        self.flags = (toint(self.bytes[oft + 0]) << 8) + toint(self.bytes[oft + 1])
        self.klass = (toint(self.bytes[oft + 2]) << 8) + toint(self.bytes[oft + 3])
        self.super = (toint(self.bytes[oft + 4]) << 8) + toint(self.bytes[oft + 5])

        cnt = (toint(self.bytes[oft + 6]) << 8) + toint(self.bytes[oft + 7])
        calc = lambda x: (toint(self.bytes[oft + x + 8]) << 8) + toint(self.bytes[oft + x + 9])
        self.interfaces = [calc(index) for index in range(cnt)]
        self.offset += 10

    def __parse_attribute(self, field):
        pass


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
    parser = PyParser(bytes)
    pyobject = parser.parse()
    print("execution complete")

