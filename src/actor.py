class Actor(object):
    def __init__(self, context):
        self.context = context

    def run(self):
        raise NotImplementedError('Implement this method')

    def render(self):
        raise NotImplementedError('Implement this method')
