#!/usr/bin/env python

import os, sys, click
from pyjvm.rt.intrptr import Intrptr
from pyjvm.rt.klassrepo import SharedRepo
from pyjvm.utils.help import usage
from pyjvm.utils.reader import FileReader
from pyjvm.loader.parser import PyParser


def __init_repo():
    return SharedRepo()

def __init_intrptr(repo):
    return Intrptr(repo)

def __parse_klass(klass):
    bytes = FileReader.read(klass)
    parser = PyParser(bytes).parse()
    return parser.build()

@click.command()
@click.argument('klass')
@click.argument('func')
def execute(klass, func):
    repo = __init_repo()
    intrptr = __init_intrptr(repo)
    
    pyklass = __parse_klass(klass)
    repo.add(klass=pyklass)

    method = pyklass.get_method(func)
    result = intrptr.execute(method)
    print("execution complete with result: {}".format(result))


if __name__ == '__main__':
    execute()

