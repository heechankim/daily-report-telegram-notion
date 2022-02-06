class Either(object):

    def __or__(self, func):
        return self.bind(func)


class Right(Either):
    def __init__(self, context):
        self.context = context

    def bind(self, func):
        return func(self.context)
    # applies func to it context


class Left(Either):
    def __init__(self, context):
        self.context = context

    def bind(self, func):
        return Left(self.context)
    # returns itself

