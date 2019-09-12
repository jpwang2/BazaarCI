from asyncio import Event

class asyncProduct(Event):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return "asyncProduct({})".format(self.name)
