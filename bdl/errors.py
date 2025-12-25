class BDLParseError(Exception):
    def __init__(self, error, source):
        self.error = error
        self.source = source
