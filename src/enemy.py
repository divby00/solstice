from gettext import gettext as _
import math
import random


class Enemy(object):
    HORIZONTAL = 0
    VERTICAL = 1
    DIAGONAL = 2

    def __str__(self):
        return ''.join([str(self.type), ';', str(self.x), ';', str(self.y)])

    def __init__(self, type, position, game_context):
        self.level = game_context.current_level
        self.x = position[0]
        self.y = position[1]
        self.active = True
        self.type = type
        self.anim = EnemyAnimations.animations[self.type]
        self.size = self.anim.images[str(0)].get_size()
        self.direction = 1
        self.speed = random.randint(1, 4)
        self.move = random.randint(0, 1)

    def run(self):
        positions = []

        if self.move == Enemy.HORIZONTAL:
            if self.direction == 1:
                positions.append(
                    ((self.x + 15 + self.speed) / self.level.map.tilewidth, self.y / self.level.map.tileheight))
                positions.append(
                    ((self.x + 15 + self.speed) / self.level.map.tilewidth, (self.y + 8) / self.level.map.tileheight))
                positions.append(
                    ((self.x + 15 + self.speed) / self.level.map.tilewidth, (self.y + 15) / self.level.map.tileheight))

                for p in positions:
                    if self.level.is_hard(p[0], p[1]):
                        self.direction = -1
            else:
                positions.append(((self.x - self.speed) / self.level.map.tilewidth, self.y / self.level.map.tileheight))
                positions.append(
                    ((self.x - self.speed) / self.level.map.tilewidth, (self.y + 8) / self.level.map.tileheight))
                positions.append(
                    ((self.x - self.speed) / self.level.map.tilewidth, (self.y + 15) / self.level.map.tileheight))

                for p in positions:
                    if self.level.is_hard(p[0], p[1]):
                        self.direction = 1

            self.x += (self.speed * self.direction)

        elif self.move == Enemy.VERTICAL:
            if self.direction == 1:
                positions.append(
                    (self.x / self.level.map.tilewidth, (self.y + 15 + self.speed) / self.level.map.tileheight))
                positions.append(
                    ((self.x + 8) / self.level.map.tilewidth, (self.y + 15 + self.speed) / self.level.map.tileheight))
                positions.append(
                    ((self.x + 15) / self.level.map.tilewidth, (self.y + 15 + self.speed) / self.level.map.tileheight))

                for p in positions:
                    if self.level.is_hard(p[0], p[1]):
                        self.direction = -1
            else:
                positions.append((self.x / self.level.map.tilewidth, (self.y - self.speed) / self.level.map.tileheight))
                positions.append(
                    ((self.x + 8) / self.level.map.tilewidth, (self.y - self.speed) / self.level.map.tileheight))
                positions.append(
                    ((self.x + 15) / self.level.map.tilewidth, (self.y - self.speed) / self.level.map.tileheight))

                for p in positions:
                    if self.level.is_hard(p[0], p[1]):
                        self.direction = 1

            self.y += (self.speed * self.direction)

        if self.anim.counter < self.anim.frames[self.anim.active_frame].duration:
            self.anim.counter += 1
        else:
            self.anim.counter = 0

            if self.anim.active_frame < len(self.anim.frames) - 1:
                self.anim.active_frame += 1
            else:
                self.anim.active_frame = 0

    def render(self, screen):
        if self.active:
            screen.blit(self.anim.images[str(self.anim.active_frame)],
                        (self.x + 256 + self.anim.frames[self.anim.active_frame].offsetx,
                         self.y + 144 + self.anim.frames[self.anim.active_frame].offsety))

    def __cmp__(self, enemy):
        if self.x < enemy.x:
            return -1
        elif self.x > enemy.x:
            return 1
        else:
            return 0


class Jellyfish00(Enemy):
    def __init__(self, position, game_context):
        super(Jellyfish00, self).__init__('jellyfish00', position, game_context)


class Jellyfish01(Enemy):
    def __init__(self, position, game_context):
        super(Jellyfish01, self).__init__('jellyfish01', position, game_context)


class Devil00(Enemy):
    def __init__(self, position, game_context):
        super(Devil00, self).__init__('devil00', position, game_context)


class Devil01(Enemy):
    def __init__(self, position, game_context):
        super(Devil01, self).__init__('devil01', position, game_context)


class EnemyUnknownException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class EnemyBuilder(object):
    enemy_list = [
        'jellyfish00',
        'jellyfish01',
        'devil00',
        'devil01'
    ]

    @staticmethod
    def build(game_context):
        enemies = []

        try:
            level = game_context.current_level
            enemy_data = game_context.current_level.map.enemy_data
            max_enemies = 0

            # Get max enemies
            for k, v in enemy_data.iteritems():
                if 'max_enemies' in k:
                    max_enemies = int(v)

            assert max_enemies > 0

            # Get total = 100%
            total = 0
            enemy_amount = {}
            for k, v in enemy_data.iteritems():

                if k in [''.join([e, '_frequency']) for e in EnemyBuilder.enemy_list]:
                    total += int(v)
                    enemy_amount[k] = math.floor((max_enemies * int(v)) / 100)

            assert total == 100

            # Build enemies

            # To calculate the initial position of the enemy in the map, we need enemy width and height of the initial
            # frame, (usually, all enemies frames will be of the same dimensions).
            enemy_sizes = {enemy_name: anim_info.images['0'].get_size() for enemy_name, anim_info in
                           EnemyAnimations.animations.iteritems()}

            for k, v in enemy_amount.iteritems():
                for e in range(int(v)):

                    enemy_size = enemy_sizes[k.replace('_frequency', '')]
                    position = EnemyBuilder.__get_initial_position(enemy_size, level)

                    if 'jellyfish00_frequency' in k:
                        enemy = Jellyfish00(position, game_context)
                    elif 'jellyfish01_frequency' in k:
                        enemy = Jellyfish01(position, game_context)
                    elif 'devil00_frequency' in k:
                        enemy = Devil00(position, game_context)
                    elif 'devil01_frequency' in k:
                        enemy = Devil01(position, game_context)
                    else:
                        raise EnemyUnknownException(_('Unable to find enemy %s' % k))
                    enemies.append(enemy)

        except EnemyUnknownException as e:
            print(e.value)

        return enemies

    @staticmethod
    def __get_initial_position(enemy_size, level):
        '''
        Calculate enemies initial position, check here that position doesn't overwrites hard zones in
        the map information.
        '''
        found_hard_zones = True
        while found_hard_zones:
            x = random.randint(0, level.map.width * level.map.tilewidth)
            y = random.randint(0, level.map.height * level.map.tileheight)

            positions = []
            positions.append((x / level.map.tilewidth, y / level.map.tileheight))
            positions.append(((x + 8) / level.map.tilewidth, y / level.map.tileheight))
            positions.append(((x + 15) / level.map.tilewidth, y / level.map.tileheight))
            positions.append((x / level.map.tilewidth, (y + 15) / level.map.tileheight))
            positions.append(((x + 8) / level.map.tilewidth, (y + 8) / level.map.tileheight))
            positions.append(((x + 15) / level.map.tilewidth, (y + 15) / level.map.tileheight))

            found = False
            for p in positions:
                if level.is_hard(p[0], p[1]):
                    found = True

            if not found:
                found_hard_zones = False

        return x, y


class EnemyAnimations(object):
    animations = {}

    @staticmethod
    def init(game_context):
        for e in EnemyBuilder.enemy_list:
            EnemyAnimations.animations[e] = game_context.resourcemanager.get(e)


class EnemyUtils(object):
    @staticmethod
    def get_nearby_enemies(enemies, position):
        result = []
        x = position[0] - 264
        y = position[1] - 152

        for e in enemies:
            if (e.y < y + 16) and (e.y + e.size[1]) > y:
                result.append(e)

        return result
