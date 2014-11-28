class Particles(object):
    def __init__(self, context, name):
        self.spr = []
        self.context = context
        self.screen = context.scr
        self.name = name
        self.resourcemanager = context.resourcemanager
        self.x = 0
        self.y = 0
        self.active = False
        self.frame = 0
        id = 0

        while True:
            particle = self.resourcemanager.get(''.join([name, str(id)]))

            if particle is not None:
                self.spr.append(particle)
                id += 1
            else:
                break

    def render(self):
        if self.active == True:
            self.screen.virt.blit(self.spr[self.frame], (self.x, self.y))

    def run(self):
        raise NotImplementedError('Implement this method')
