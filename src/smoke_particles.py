import random

import particles


class SmokeParticles(particles.Particles):
    def __init__(self, context, name):
        super(SmokeParticles, self).__init__(context, name)
        for x in xrange(0, 300):
            particle = particles.Particle(random.randint(377, 410), random.randint(60, 120), True, random.randint(0, 2))
            self.particle_list.append(particle)

    def run(self):
        for p in self.particle_list:
            direction = random.randint(0, 1)
            if direction == 0:
                direction = -1
            p.x += random.randint(0, 2) * direction
            p.y -= random.randint(0, 2)
            if p.frame < 7:
                change_frame = random.randint(0, 2)
                if change_frame == 2:
                    p.frame += 1
            else:
                p.x = random.randint(377, 410)
                p.y = random.randint(60, 120)
                p.frame = random.randint(0, 2)

    def render(self, screen):
        for p in self.particle_list:
            screen.blit(self.spr[p.frame], (p.x, p.y))
