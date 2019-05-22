

class KlassNotFoundException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "KlassNotFoundException(msg={})".format(self.message)
