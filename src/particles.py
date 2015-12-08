import random


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

    def render(self, screen):
        raise NotImplementedError('Implement this method')

    def run(self):
        raise NotImplementedError('Implement this method')


class EnemyExplosionParticles(Particles):
    def __init__(self, context, name):
        super(EnemyExplosionParticles, self).__init__(context, name)

    def generate(self, position):
        for x in xrange(0, 10):
            particle = Particle(random.randint(position[0] - 5, position[1] - 5),
                                random.randint(position[2] - 5, position[3] - 5),
                                True, random.randint(-5, 0))
            self.particle_list.append(particle)

    def run(self):
        for p in self.particle_list:
            if p.frame < 6:
                p.frame += 1
            else:
                self.particle_list.remove(p)

    def render(self, screen):
        for p in self.particle_list:
            if -1 < p.frame < 6:
                screen.blit(self.spr[p.frame], (p.x, p.y))


class ExplosionParticles(Particles):
    def __init__(self, context, name):
        super(ExplosionParticles, self).__init__(context, name)

    def generate(self, position):
        for x in xrange(0, 20):
            particle = Particle(random.randint(position[0] - 16, position[1] - 16),
                                random.randint(position[2] - 16, position[3] - 16),
                                True, random.randint(-6, 0))
            self.particle_list.append(particle)

    def run(self):
        for p in self.particle_list:
            if p.frame < 6:
                p.frame += 1
            else:
                self.particle_list.remove(p)

    def render(self, screen):
        for p in self.particle_list:
            if -1 < p.frame < 6:
                screen.blit(self.spr[p.frame], (p.x, p.y))


class PlayerCrapParticles(Particles):
    def __init__(self, context, name):
        super(PlayerCrapParticles, self).__init__(context, name)

    def generate(self, position):
        for x in xrange(0, 5):
            particle = Particle(random.randint(position[0], position[1]),
                                random.randint(position[2], position[3]),
                                True, random.randint(-4, 0))
            self.particle_list.append(particle)

    def run(self):
        for p in self.particle_list:
            if p.frame < 4:
                p.frame += 1
                p.y += 2
            else:
                self.particle_list.remove(p)

    def render(self, screen):
        for p in self.particle_list:
            if -1 < p.frame < 4:
                screen.blit(self.spr[p.frame], (p.x, p.y))


class SmokeParticles(Particles):
    def __init__(self, context, name):
        super(SmokeParticles, self).__init__(context, name)
        for x in xrange(0, 200):
            particle = Particle(random.randint(377, 410), random.randint(110, 122), True, random.randint(0, 2))
            self.particle_list.append(particle)

    def run(self):
        for p in self.particle_list:
            direction = random.randint(0, 1)
            if direction == 0:
                direction = -1
            p.x += random.randint(0, 2) * direction
            p.y -= random.randint(0, 2)
            if p.frame < 7:
                change_frame = random.randint(0, 4)
                if change_frame == 2:
                    p.frame += 1
            else:
                p.x = random.randint(377, 410)
                p.y = random.randint(110, 122)
                p.frame = random.randint(0, 2)

    def render(self, screen):
        for p in self.particle_list:
            screen.blit(self.spr[p.frame], (p.x, p.y))


class BeamParticles(Particles):
    def __init__(self, context, name):
        super(BeamParticles, self).__init__(context, name)

    def generate(self, position):
        for x in xrange(0, 20):
            particle = Particle(random.randint(position[0], position[1]), random.randint(position[2], position[3]),
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


class EnemyBeamParticles(Particles):
    def __init__(self, context, name):
        super(EnemyBeamParticles, self).__init__(context, name)

    def generate(self, position):
        for x in xrange(0, 10):
            particle = Particle(random.randint(position[0], position[1]), random.randint(position[2], position[3]),
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
