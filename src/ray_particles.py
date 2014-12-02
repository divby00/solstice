import random

import particles


class RayParticles(particles.Particles):
    def __init__(self, context, name, position):
        super(RayParticles, self).__init__(context, name)
        for x in xrange(0, 10):
            particle = particles.Particle(random.randint(position[0], position[1]),
                                          random.randint(position[2], position[3]),
                                          True, random.randint(-4, 0))
            self.particle_list.append(particle)

    def run(self):
        for p in self.particle_list:
            if p.frame < 3:
                p.frame += 1
            else:
                self.particle_list.remove(p)

    def render(self, screen):
        for p in self.particle_list:
            if -1 < p.frame < 3:
                screen.blit(self.spr[p.frame], (p.x, p.y))
