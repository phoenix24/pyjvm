#!//usr/bin/env python

import os, sys
from pyjvm.rt.intrptr import Intrptr
from pyjvm.rt.klassrepo import SharedRepo
from pyjvm.utils.help import usage
from pyjvm.utils.reader import FileReader
from pyjvm.loader.parser import PyParser


if __name__ == '__main__':
    args = sys.argv
    if len(args) >= 2 and not args[1].endswith(".class"):
        usage()
        
    bytes = FileReader.read(args[1])
    parser = PyParser(bytes).parse()
    pyklass = parser.build()

    repo = SharedRepo()
    repo.add(klass=pyklass)

    intrptr = Intrptr(repo)
    method = pyklass.get_method("foo:()I")

    result = intrptr.execute(method)
    print("execution complete with result: {}".format(result))

