import random

import particles


class SmokeParticles(particles.Particles):
    def __init__(self, context, name):
        super(SmokeParticles, self).__init__(context, name)
        for x in xrange(0, 70):
            particle = particles.Particle(random.randint(180, 212), random.randint(70, 116), True, random.randint(0, 7))
            self.particle_list.append(particle)

    def run(self):
        for p in self.particle_list:
            '''
            if p.x < 256:
                p.x += 1
            else:
                p.x = 0
            '''
            if p.frame < 7:
                p.frame += 1
            else:
                p.frame = 0

    def render(self):
        for p in self.particle_list:
            self.screen.virt.blit(self.spr[p.frame], (p.x, p.y))
