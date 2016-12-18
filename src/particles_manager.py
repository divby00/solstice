class ParticlesManager(object):
    def __init__(self):
        self._particles = {}

    '''
    Public methods
    '''

    def get(self, name):
        return self._particles[name]

    def register_particles(self, particles):
        self._particles[particles.name] = particles

    def unregister_particles(self, name):
        del (self._particles[name])

    def run(self):
        for key in self._particles:
            self._particles[key].run()

    def render(self, screen):
        for key in self._particles:
            self._particles[key].render(screen)
