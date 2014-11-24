import actor


class Laser(actor.Actor):
    def __init__(self, context, position, direction):
        super(Laser, self).__init__(context)
        self.position = position
        self.animation = 4
        self.direction = direction

    def run(self):
        if self.animation > 0:
            self.animation -= 1

    def render(self):

        if self.direction == 1:
            if self.animation >= 3:
                self.context.scr.virt.blit(self.context.laser_spr[0], (self.position[0], self.position[1]))
                for i in xrange(self.position[0] + 8, 256, 8):
                    self.context.scr.virt.blit(self.context.laser_spr[3], (i, self.position[1]))
            if self.animation == 2:
                self.context.scr.virt.blit(self.context.laser_spr[1], (self.position[0], self.position[1]))
                for i in xrange(self.position[0] + 8, 256, 8):
                    self.context.scr.virt.blit(self.context.laser_spr[4], (i, self.position[1]))
            if self.animation == 1:
                self.context.scr.virt.blit(self.context.laser_spr[2], (self.position[0], self.position[1]))
                for i in xrange(self.position[0] + 8, 256, 8):
                    self.context.scr.virt.blit(self.context.laser_spr[5], (i, self.position[1]))
        else:
            if self.animation >= 3:
                self.context.scr.virt.blit(self.context.laser_spr[8], (self.position[0] - 24, self.position[1]))
                for i in xrange(0, self.position[0] - 24, 8):
                    self.context.scr.virt.blit(self.context.laser_spr[3], (i, self.position[1]))
            if self.animation == 2:
                self.context.scr.virt.blit(self.context.laser_spr[7], (self.position[0] - 24, self.position[1]))
                for i in xrange(0, self.position[0] - 24, 8):
                    self.context.scr.virt.blit(self.context.laser_spr[4], (i, self.position[1]))
            if self.animation == 1:
                self.context.scr.virt.blit(self.context.laser_spr[6], (self.position[0] - 24, self.position[1]))
                for i in xrange(0, self.position[0] - 24, 8):
                    self.context.scr.virt.blit(self.context.laser_spr[5], (i, self.position[1]))


class Player(actor.Actor):
    def __init__(self, context, current_level):
        super(Player, self).__init__(context)
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.absolute_x = 0
        self.absolute_y = 0
        self.animation = 0
        self.direction = 0
        self.sprites = []
        self.laser_spr = []
        self.view_port = [256, 144]

        player = [
            'player0', 'player1', 'player2', 'player3',
            'player4', 'player5', 'player6', 'player7',
            'player8', 'player9', 'player10', 'player11',
            'player12', 'player13', 'player14'
        ]

        laser = [
            'shoot0', 'shoot1', 'shoot2',
            'shoot3', 'shoot4', 'shoot5',
            'shoot6', 'shoot7', 'shoot8'
        ]

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
        self.x = self.current_level.start_point[0] * self.current_level.map.tilewidth
        self.y = self.current_level.start_point[1] * self.current_level.map.tileheight
        self.absolute_x = self.x
        self.absolute_y = self.y
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

    def render(self):
        self.context.scr.virt.blit(self.sprites[self.animation],
                                   (self.x % self.view_port[0],
                                    self.y % self.view_port[1]))
        for l in self.lasers:
            l.render()

    def shoot(self):
        laser = Laser(self.context, (self.x + 16, self.y, 256), self.direction)
        self.lasers.append(laser)

    def check_right_collision(self, level):

        calculated_x = int((self.absolute_x + self.w) / level.map.tilewidth)
        calculated_y = []
        calculated_y.insert(0, int(self.absolute_y / level.map.tilewidth))
        calculated_y.insert(1, int((self.absolute_y + ((self.h / 2) - 1)) /
                                   level.map.tilewidth))
        calculated_y.insert(2, int((self.absolute_y + (self.h - 1)) /
                                   level.map.tilewidth))

        for l in level.layers:
            if l.name == 'special':
                for a in calculated_y:
                    if l.get_gid(calculated_x, a) == 520:
                        return True

        return False

    def check_left_collision(self, level):
        calculated_x = int((self.absolute_x - 1) / level.map.tilewidth)
        calculated_y = []
        calculated_y.insert(0, int(self.absolute_y / level.map.tileheight))
        calculated_y.insert(1, int((self.absolute_y + ((self.h / 2) - 1)) /
                                   level.map.tileheight))
        calculated_y.insert(2, int((self.absolute_y + (self.h - 1)) /
                                   level.map.tileheight))

        for l in level.layers:
            if l.name == 'special':
                for a in calculated_y:
                    if l.get_gid(calculated_x, a) == 520:
                        return True

        return False

    def check_upper_collision(self, level):
        calculated_y = int((self.absolute_y - 1) / level.map.tileheight)
        calculated_x = []
        calculated_x.insert(0, int(self.absolute_x / level.map.tilewidth))
        calculated_x.insert(1, int((self.absolute_x + ((self.w / 2) - 1)) /
                                   level.map.tilewidth))
        calculated_x.insert(2, int((self.absolute_x + (self.w - 1)) /
                                   level.map.tilewidth))

        for l in level.layers:
            if l.name == 'special':
                for i in calculated_x:
                    if l.get_gid(i, calculated_y) == 520:
                        return True

        return False

    def check_bottom_collision(self, level):

        calculated_y = int((self.absolute_y + self.h) / level.map.tileheight)
        calculated_x = []
        calculated_x.insert(0, int(self.absolute_x / level.map.tilewidth))
        calculated_x.insert(1, int((self.absolute_x + ((self.w / 2) - 1)) /
                                   level.map.tilewidth))
        calculated_x.insert(2, int((self.absolute_x + (self.w - 1)) /
                                   level.map.tilewidth))

        for l in level.layers:
            if l.name == 'special':
                for i in calculated_x:
                    if l.get_gid(i, calculated_y) == 520:
                        return True

        return False
