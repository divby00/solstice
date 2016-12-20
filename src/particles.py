import random


class Particle(object):
    def __init__(self, x=0, y=0, frame=0):
        self._x = x
        self._y = y
        self._frame = frame

    '''
    Public methods
    '''

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value


class Particles(object):
    def __init__(self, resource_manager, name):
        self._name = name
        self._sprites = []
        self._particle_list = []
        particle_id = 0
        while True:
            if resource_manager.exists(''.join([name, str(particle_id)])):
                particle = resource_manager.get(''.join([name, str(particle_id)]))
                if particle is not None:
                    self._sprites.append(particle)
                    particle_id += 1
            else:
                break

    '''
    Public methods
    '''

    def render(self, screen):
        raise NotImplementedError('Implement this method')

    def run(self):
        raise NotImplementedError('Implement this method')

    @property
    def name(self):
        return self._name


class EnemyExplosionParticles(Particles):
    def __init__(self, resource_manager, name):
        super(EnemyExplosionParticles, self).__init__(resource_manager, name)

    '''
    Public methods
    '''

    def generate(self, position):
        for x in xrange(0, 10):
            particle = Particle(random.randint(position[0] - 5, position[1] - 5),
                                random.randint(position[2] - 5, position[3] - 5),
                                random.randint(-5, 0))
            self._particle_list.append(particle)

    def run(self):
        for particle in self._particle_list:
            if particle.frame < 6:
                particle.frame += 1
            else:
                self._particle_list.remove(particle)

    def render(self, screen):
        for particle in self._particle_list:
            if -1 < particle.frame < 6:
                screen.blit(self._sprites[particle.frame], (particle.x, particle.y))


class ExplosionParticles(Particles):
    def __init__(self, resource_manager, name):
        super(ExplosionParticles, self).__init__(resource_manager, name)

    '''
    Public methods
    '''

    def generate(self, position):
        for x in xrange(0, 20):
            particle = Particle(random.randint(position[0] - 16, position[1] - 16),
                                random.randint(position[2] - 16, position[3] - 16),
                                random.randint(-6, 0))
            self._particle_list.append(particle)

    def run(self):
        for particle in self._particle_list:
            if particle.frame < 6:
                particle.frame += 1
            else:
                self._particle_list.remove(particle)

    def render(self, screen):
        for particle in self._particle_list:
            if -1 < particle.frame < 6:
                screen.blit(self._sprites[particle.frame], (particle.x, particle.y))


class PlayerCrapParticles(Particles):
    def __init__(self, resource_manager, name):
        super(PlayerCrapParticles, self).__init__(resource_manager, name)

    '''
    Public methods
    '''

    def generate(self, position):
        for x in xrange(0, 10):
            particle = Particle(random.randint(position[0], position[1]),
                                random.randint(position[2], position[3]),
                                random.randint(-4, 0))
            self._particle_list.append(particle)

    def run(self):
        for particle in self._particle_list:
            if particle.frame < 4:
                particle.frame += 1
                particle.y += random.randint(1, 4)
            else:
                self._particle_list.remove(particle)

    def render(self, screen):
        for particle in self._particle_list:
            if -1 < particle.frame < 4:
                screen.blit(self._sprites[particle.frame], (particle.x, particle.y))


class RespawnParticles(Particles):
    def __init__(self, resource_manager, name):
        super(RespawnParticles, self).__init__(resource_manager, name)

    '''
    Public methods
    '''

    def generate(self, position):
        for x in xrange(0, 50):
            dest_position = random.randint(position[0], position[1]), \
                            random.randint(position[2], position[3])
            speed = (random.uniform(-2, 2),
                     random.uniform(-2, 2))
            iterations = random.randint(25, 50)
            source_position = (dest_position[0] + (iterations * speed[0]),
                               dest_position[1] + (iterations * speed[1]))
            particle = Particle(source_position[0], source_position[1], random.randint(-50, 0))
            particle.iterations = iterations
            particle.speed = speed
            particle.dest_position = dest_position
            self._particle_list.append(particle)

    def run(self):
        for particle in self._particle_list:
            if particle.iterations > 0:
                particle.x -= particle.speed[0]
                particle.y -= particle.speed[1]

                if particle.x + 2 >= particle.dest_position[0] \
                        and particle.x <= particle.dest_position[0] + 2 \
                        and particle.y + 2 >= particle.dest_position[1] \
                        and particle.y <= particle.dest_position[1] + 2:
                    self._particle_list.remove(particle)
            else:
                self._particle_list.remove(particle)

    def render(self, screen):
        for particle in self._particle_list:
            screen.blit(self._sprites[random.randint(0, 5)], (particle.x, particle.y))


class PlayerSmokeParticles(Particles):
    def __init__(self, resource_manager, name):
        super(PlayerSmokeParticles, self).__init__(resource_manager, name)

    '''
    Public methods
    '''

    def generate(self, position):
        for x in xrange(0, 5):
            particle = Particle(random.randint(position[0], position[1]),
                                random.randint(position[2], position[3]),
                                random.randint(-4, 0))
            self._particle_list.append(particle)

    def run(self):
        for particle in self._particle_list:
            if particle.frame < 4:
                particle.frame += 1
                particle.y += 1
            else:
                self._particle_list.remove(particle)

    def render(self, screen):
        for p in self._particle_list:
            if -1 < p.frame < 4:
                screen.blit(self._sprites[p.frame], (p.x, p.y))


class SmokeParticles(Particles):
    def __init__(self, resource_manager, name):
        super(SmokeParticles, self).__init__(resource_manager, name)
        for x in xrange(0, 200):
            particle = Particle(random.randint(377, 410), random.randint(110, 122),
                                random.randint(0, 2))
            self._particle_list.append(particle)

    '''
    Public methods
    '''

    def run(self):
        for particle in self._particle_list:
            direction = random.randint(0, 1)
            if direction == 0:
                direction = -1
            particle.x += random.randint(0, 2) * direction
            particle.y -= random.randint(0, 2)
            if particle.frame < 7:
                change_frame = random.randint(0, 4)
                if change_frame == 2:
                    particle.frame += 1
            else:
                particle.x = random.randint(377, 410)
                particle.y = random.randint(110, 122)
                particle.frame = random.randint(0, 2)

    def render(self, screen):
        for particle in self._particle_list:
            screen.blit(self._sprites[particle.frame], (particle.x, particle.y))


class BeamParticles(Particles):
    def __init__(self, resource_manager, name):
        super(BeamParticles, self).__init__(resource_manager, name)

    def generate(self, position):
        for x in xrange(0, 20):
            particle = Particle(random.randint(position[0], position[1]),
                                random.randint(position[2], position[3]),
                                random.randint(-4, 0))
            self._particle_list.append(particle)

    def run(self):
        for particle in self._particle_list:
            if particle.frame < 3:
                particle.frame += 1
            else:
                self._particle_list.remove(particle)

    def render(self, screen):
        for particle in self._particle_list:
            if -1 < particle.frame < 3:
                screen.blit(self._sprites[particle.frame], (particle.x, particle.y))


class EnemyBeamParticles(Particles):
    def __init__(self, resource_manager, name):
        super(EnemyBeamParticles, self).__init__(resource_manager, name)

    def generate(self, position):
        for x in xrange(0, 10):
            particle = Particle(random.randint(position[0], position[1]),
                                random.randint(position[2], position[3]),
                                random.randint(-4, 0))
            self._particle_list.append(particle)

    def run(self):
        for particle in self._particle_list:
            if particle.frame < 3:
                particle.frame += 1
            else:
                self._particle_list.remove(particle)

    def render(self, screen):
        for particle in self._particle_list:
            if -1 < particle.frame < 3:
                screen.blit(self._sprites[particle.frame], (particle.x, particle.y))
