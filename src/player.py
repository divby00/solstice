import actor


class Laser(actor.Actor):
    def __init__(self, context, position, direction):
        super(Laser, self).__init__(context)
        self.active = True
        self.animation = 4
        self.direction = direction
        self.limit = [0, 0]
        self.position = position

    def run(self):
        if self.animation > 0:
            self.animation -= 1

    def render(self, screen):
        if self.direction == 1:
            if self.animation >= 3:
                screen.blit(self.context.laser_spr[0], (self.position[0], self.position[1]))
                for i in xrange(self.position[0] + 8, self.position[2], 4):
                    screen.blit(self.context.laser_spr[3], (i, self.position[1]))
            if self.animation == 2:
                screen.blit(self.context.laser_spr[1], (self.position[0], self.position[1]))
                for i in xrange(self.position[0] + 8, self.position[2], 4):
                    screen.blit(self.context.laser_spr[4], (i, self.position[1]))
            if self.animation == 1:
                screen.blit(self.context.laser_spr[2], (self.position[0], self.position[1]))
                for i in xrange(self.position[0] + 8, self.position[2], 4):
                    screen.blit(self.context.laser_spr[5], (i, self.position[1]))
        else:
            if self.animation >= 3:
                screen.blit(self.context.laser_spr[8], (self.position[0], self.position[1]))
                for i in xrange(self.position[0] - 4, self.position[2], -4):
                    screen.blit(self.context.laser_spr[3], (i, self.position[1]))
            if self.animation == 2:
                screen.blit(self.context.laser_spr[7], (self.position[0], self.position[1]))
                for i in xrange(self.position[0] - 4, self.position[2], -4):
                    screen.blit(self.context.laser_spr[4], (i, self.position[1]))
            if self.animation == 1:
                screen.blit(self.context.laser_spr[6], (self.position[0], self.position[1]))
                for i in xrange(self.position[0] - 4, self.position[2], -4):
                    screen.blit(self.context.laser_spr[5], (i, self.position[1]))


class Player(actor.Actor):
    def __init__(self, context, current_level):
        super(Player, self).__init__(context)
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.animation = 0
        self.direction = 0
        self.shoot_avail = True
        self.shoot_avail_counter = 0
        self.sprites = []
        self.laser_spr = []
        self.particlesmanager = context.particlesmanager

        player = ['player0', 'player1', 'player2', 'player3',
                  'player4', 'player5', 'player6', 'player7',
                  'player8', 'player9', 'player10', 'player11',
                  'player12', 'player13', 'player14']

        laser = ['shoot0', 'shoot1', 'shoot2',
                 'shoot3', 'shoot4', 'shoot5',
                 'shoot6', 'shoot7', 'shoot8']

        self.lasers = []

        for p in xrange(0, len(player)):
            self.sprites.insert(p, self.context.resourcemanager.get(player[p]))

        for l in xrange(0, len(laser)):
            self.laser_spr.insert(l, self.context.resourcemanager.get(laser[l]))

        self.current_level = current_level
        self.context.laser_spr = self.laser_spr

    def on_start(self):
        self.w = self.sprites[0].get_width()
        self.h = self.sprites[0].get_height()
        self.x = ((self.current_level.start_point[0] * 8) + 256 + 8)
        self.y = ((self.current_level.start_point[1] * 8) + 144 + 8)
        self.animation = 0
        self.direction = 1
        self.firing = False
        self.lasers = []

    def run(self):
        self.animation += self.direction

        if self.animation == 15:
            self.animation = 0
        if self.animation < 0:
            self.animation = 14

        if self.firing:
            self.shoot()
            self.firing = False

        for l in self.lasers:
            l.run()

            if l.animation == 0:
                self.lasers.remove(l)

        if not self.shoot_avail:
            self.shoot_avail_counter += 1
            
            if self.shoot_avail_counter == 6:
                self.shoot_avail = True
                self.shoot_avail_counter = 0

    def render(self, screen):
        screen.blit(self.sprites[self.animation], (self.x - 8, self.y - 8))
        for l in self.lasers:
            l.render(screen)

    def shoot(self):
        laser = None
        self.shoot_avail = False
        if self.direction == 1:
            colision_x = self.get_laser_right_collision()
            beam_particles = self.particlesmanager.get('hit')
            beam_particles.generate((self.x + 4 + colision_x, self.x + 12 + colision_x, self.y - 8, self.y))
            laser = Laser(self.context, (self.x + 8, self.y - 8, self.x + 8 + colision_x), self.direction)
        else:
            colision_x = self.get_laser_left_collision()
            beam_particles = self.particlesmanager.get('hit')
            beam_particles.generate((self.x - 20 - colision_x, self.x - 12 - colision_x, self.y - 8, self.y))
            laser = Laser(self.context, (self.x - 16, self.y - 8, self.x - 16 - colision_x), self.direction)

        self.lasers.append(laser)

    def get_laser_right_collision(self):
        for l in self.current_level.layers:
            if l.name == 'special':
                calculated_x = int((self.x - 8 + self.w) / self.current_level.map.tilewidth) - 32
                calculated_x_limit = int((self.x + self.w + 248) / self.current_level.map.tilewidth) - 32
                calculated_y = (self.y) / self.current_level.map.tileheight - 18
                for x in xrange(calculated_x, calculated_x_limit):
                    if self.current_level.is_hard(x, calculated_y):
                        a = abs(x - calculated_x) * 8
                        if self.x % 8 is not 0:
                            a -= 4
                        return a
        return 256

    def get_laser_left_collision(self):
        for l in self.current_level.layers:
            if l.name == 'special':
                calculated_x = int((self.x - 16) / self.current_level.map.tilewidth) - 32
                calculated_x_limit = int((self.x - 264) / self.current_level.map.tilewidth) - 32
                calculated_y = (self.y) / self.current_level.map.tileheight - 18
                for x in xrange(calculated_x, calculated_x_limit, -1):
                    if self.current_level.is_hard(x, calculated_y):
                        a = abs(x - calculated_x) * 8
                        if self.x % 8 is 0:
                            a -= 4
                        return a
        return 256

    def check_right_collision(self, level):
        calculated_x = int(((self.x - 8 ) + self.w) / level.map.tilewidth) - 32
        calculated_y = []
        calculated_y.insert(0, int((self.y - 8) / level.map.tilewidth) - 18)
        calculated_y.insert(1, int(((self.y - 8) + ((self.h / 2) - 1)) /
                                   level.map.tilewidth) - 18)
        calculated_y.insert(2, int(((self.y - 8) + (self.h - 1)) /
                                   level.map.tilewidth) - 18)
        for l in level.layers:
            if l.name == 'special':
                result = False
                for a in calculated_y:
                    if self.current_level.is_hard(calculated_x, a):
                        result = True

        return result

    def check_left_collision(self, level):
        calculated_x = int((self.x - 9) / level.map.tilewidth) - 32
        calculated_y = []
        calculated_y.insert(0, int(self.y - 8 / level.map.tileheight) - 18)
        calculated_y.insert(1, int((self.y - 8 + ((self.h / 2) - 1)) /
                                   level.map.tileheight) - 18)
        calculated_y.insert(2, int((self.y - 8 + (self.h - 1)) /
                                   level.map.tileheight) - 18)
        for l in level.layers:
            if l.name == 'special':
                result = False
                for a in calculated_y:
                    if self.current_level.is_hard(calculated_x, a):
                        result = True

        return result

    def check_upper_collision(self, level):
        calculated_y = int((self.y - 9) / level.map.tileheight) - 18
        calculated_x = []
        calculated_x.insert(0, int((self.x - 8) / level.map.tilewidth) - 32)
        calculated_x.insert(1, int(((self.x - 8) + ((self.w / 2) - 1)) /
                                   level.map.tilewidth) - 32)
        calculated_x.insert(2, int(((self.x - 8) + (self.w - 1)) /
                                   level.map.tilewidth) - 32)

        for l in level.layers:
            if l.name == 'special':
                result = False
                for i in calculated_x:
                    if self.current_level.is_hard(i, calculated_y):
                        result = True

        return result

    def check_bottom_collision(self, level):

        calculated_y = int(((self.y - 8) + self.h) / level.map.tileheight) - 18
        calculated_x = []
        calculated_x.insert(0, int((self.x - 8) / level.map.tilewidth) - 32)
        calculated_x.insert(1, int(((self.x - 8)+ ((self.w / 2) - 1)) /
                                   level.map.tilewidth) - 32)
        calculated_x.insert(2, int(((self.x - 8) + (self.w - 1)) /
                                   level.map.tilewidth) - 32)

        for l in level.layers:
            if l.name == 'special':
                result = False
                for i in calculated_x:
                    if self.current_level.is_hard(i, calculated_y):
                        result = True

        return result
