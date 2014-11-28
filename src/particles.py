class Particle(object):
    def __init__(self, x=0, y=0, active=True, frame=0):
        self.x = x
        self.y = y
        self.active = active
        self.frame = frame

class Particles(object):
    def __init__(self, context, name):
        self.spr = []
        self.context = context
        self.screen = context.scr
        self.name = name
        self.resourcemanager = context.resourcemanager
        self.particle_list = []
        id = 0

        while True:
            if self.resourcemanager.exists(''.join([name, str(id)])):
                particle = self.resourcemanager.get(''.join([name, str(id)]))
                if particle is not None:
                    self.spr.append(particle)
                    id += 1
            else:
                break

    def render(self):
        raise NotImplementedError('Implement this method')

    def run(self):
        raise NotImplementedError('Implement this method')
