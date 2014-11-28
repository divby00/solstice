class ParticlesManager(object):
    def __init__(self):
        self.particles = {}

    def register_particles(self, particles):
        self.particles[particles.name] = particles

    def unregister_particles(self, name):
        del (self.particles[name])

    def run(self):
        for key in self.particles:
            self.particles[key].run()

    def render(self, screen):
        for key in self.particles:
            self.particles[key].render(screen)
