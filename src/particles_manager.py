class ParticlesManager(object):
    def __init__(self):
        self.particles = {}

    def register_particles(self, particle):
        self.particles[particle.name] = particle

    def unregister_particles(self, name):
        del (self.particles[name])

    def run(self):
        for key in self.particles:
            self.particles[key].run()

    def render(self):
        for key in self.particles:
            self.particles[key].render()
