#!//usr/bin/env python

import os, sys

def usage():
    helptxt = """ \
    usage:
    $ ./pyjvm.py <filename.class>
    """
    print(helptxt)

class PyField(object):
    def __init__(self):
        # name
        # type
        # flags
        # klass
        pass

class PyMethod(object):
    def __init__(self):
        # class
        # name-and-type
        # bytecode
        # signature
        # flags
        # arguments
        pass

class PyKlass(object):
    def __init__(self, ):
        #class
        #super-classes
        #methods
        #fields
        #static fields
        pass

class PyKonst(object):
    pass

class PyKPType(object):
    def __init__(self, val, type, sep = ""):
        self.val = val
        self.sep = sep
        self.type = type

class PyKPEntry(object):
    def __init__(self):
        pass

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

def toint(byte):
    return int.from_bytes(
        byte, 
        byteorder='little'
    )
    
class PyParser(object):
    def __init__(self, bytes):
        self.bytes = bytes
        self.offset = 0

        self.major = None
        self.minor = None
        self.pool_count = -1
        
        self.kptable = []
        self.kptypes = []
        self.kpentrys = []
        self.kpfields = []
        self.kpmethods = []

    def parse(self):
        self.__init()
        self.__header()
        self.__constant_pool()
        self.__basic_type_info()
        self.__fields()
        self.__methods()
        return self.klass()

    def klass(self):
        pass

    def __init(self):
        self.kptable.append(PyKPType(1, "UTF8"))
        self.kptable.append(PyKPType(3, "INTEGER"))
        self.kptable.append(PyKPType(4, "FLOAT"))
        self.kptable.append(PyKPType(5, "LONG"))
        self.kptable.append(PyKPType(6, "DOUBLE"))
        self.kptable.append(PyKPType(7, "CLASS"))
        self.kptable.append(PyKPType(8, "STRING"))
        self.kptable.append(PyKPType(9, "FIELDREF", "."))
        self.kptable.append(PyKPType(10, "METHODREF", "."))
        self.kptable.append(PyKPType(11, "INTERFACE_METHODREF"))
        self.kptable.append(PyKPType(12, "NAMEANDTYPE", ":"))
        self.kptable.append(PyKPType(15, "METHODHANDLE"))
        self.kptable.append(PyKPType(16, "METHODTYPE"))
        self.kptable.append(PyKPType(18, "INVOKEDYNAMIC"))

    def __header(self):
        bytes = self.bytes[:4]
        header = [0xca, 0xfe, 0xba, 0xbe]
        for actual, expected in zip(bytes, header):
            actual = toint(actual)
            if actual != expected: 
                raise Exception("invalid header. expected:%s found:%s" % (expected, actual))

        self.minor = toint(self.bytes[5]) + toint(self.bytes[6])
        self.major = toint(self.bytes[7]) + toint(self.bytes[8])
        self.pool_count = toint(self.bytes[9]) + toint(self.bytes[10])
        self.offset += 10

    def __fields(self):
        pass

    def __methods(self):
        pass

    def __constant_pool(self):
        
        pass

    def __basic_type_info(self):
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

