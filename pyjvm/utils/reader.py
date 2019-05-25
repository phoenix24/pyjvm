import os


class PyReader(object):
    @staticmethod
    def read(file):
        raise NotImplementedError


class FileReader(PyReader):    
    @staticmethod
    def read(file):
        bytes = []
        with open(file, 'rb') as bfile:
            byte = bfile.read(1)
            while byte:
                bytes.append(byte)
                byte = bfile.read(1)
        return bytes
