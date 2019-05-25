

class PyTypeNotFoundException(Exception):
    def __init__(self, message, exception=None):
        self.ex = exception
        self.message = message

    def __str__(self):
        return "PyTypeNotFoundException(msg={}, exception={})".format(self.message, self.ex)


class PyKlassNotFoundException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "PyKlassNotFoundException(msg={})".format(self.message)


class PyIllegalArgumentException(Exception):
    def __init__(self, message, exception=None):
        self.ex = exception
        self.message = message

    def __str__(self):
        return "PyIllegalArgumentException(msg={}, exception={})".format(self.message, self.ex)


class PyIllegalOpcodeFound(Exception):
    def __init__(self, message, exception=None):
        self.ex = exception
        self.message = message

    def __str__(self):
        return "PyIllegalArgumentException(msg={}, exception={})".format(self.message, self.ex)


class PyVMIllegalStateException(Exception):
    def __init__(self, message, exception=None):
        self.ex = exception
        self.message = message

    def __str__(self):
        return "PyVMIllegalStateException(msg={}, exception={})".format(self.message, self.ex)