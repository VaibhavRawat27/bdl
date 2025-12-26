# bdl/context.py
class Context:
    def __init__(self):
        self.tables = {}   # in-memory tables
        self.active = None

context = Context()
