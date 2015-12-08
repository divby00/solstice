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
        self.game_context = game_context
        self.level = game_context.current_level
        self.sound_player = game_context.sound_player
        self.x = position[0]
        self.y = position[1]
        self.type = type
        self.anim = EnemyAnimations.animations[self.type]
        self.anim_respawn = EnemyAnimations.animations[self.type + '_init']
        self.size = self.anim.images[str(0)].get_size()
        self.init_enemy()

    def init_enemy(self):
        self.anim.active_frame = 0
        self.anim_respawn.active_frame = 0
        self.shock_counter = 0
        self.active = True
        self.change_movement = 0
        self.respawn = False
        self.respawn_counter = random.randint(50, 200)
        self.direction = 1
        self.speed = random.randint(1, 4)
        self.move = random.randint(0, 1)
        self.__adjust_energy()

    def __adjust_energy(self):
        if self.type == 'jellyfish00':
            self.energy = 2
        elif self.type == 'devil00':
            self.energy = 2
        elif self.type == 'jellyfish01':
            self.energy = 3
        elif self.type == 'devil01':
            self.energy = 1

    def __get_collision_list(self, facing):
        if facing == 'left':
            return self.__get_left_collision_list()
        elif facing == 'right':
            return self.__get_right_collision_list()
        elif facing == 'top':
            return self.__get_upper_collision_list()
        else:
            return self.__get_bottom_collision_list()

    def __get_left_collision_list(self):
        positions = []
        positions.append(((self.x - self.speed) / self.level.map.tilewidth, self.y / self.level.map.tileheight))
        positions.append(((self.x - self.speed) / self.level.map.tilewidth, (self.y + 8) / self.level.map.tileheight))
        positions.append(((self.x - self.speed) / self.level.map.tilewidth, (self.y + 15) / self.level.map.tileheight))
        return positions

    def __get_right_collision_list(self):
        positions = []
        positions.append(((self.x + 15 + self.speed) / self.level.map.tilewidth, self.y / self.level.map.tileheight))
        positions.append(
            ((self.x + 15 + self.speed) / self.level.map.tilewidth, (self.y + 8) / self.level.map.tileheight))
        positions.append(
            ((self.x + 15 + self.speed) / self.level.map.tilewidth, (self.y + 15) / self.level.map.tileheight))
        return positions

    def __get_upper_collision_list(self):
        positions = []
        positions.append((self.x / self.level.map.tilewidth, (self.y - self.speed) / self.level.map.tileheight))
        positions.append(((self.x + 8) / self.level.map.tilewidth, (self.y - self.speed) / self.level.map.tileheight))
        positions.append(((self.x + 15) / self.level.map.tilewidth, (self.y - self.speed) / self.level.map.tileheight))
        return positions

    def __get_bottom_collision_list(self):
        positions = []
        positions.append((self.x / self.level.map.tilewidth, (self.y + 15 + self.speed) / self.level.map.tileheight))
        positions.append(
            ((self.x + 8) / self.level.map.tilewidth, (self.y + 15 + self.speed) / self.level.map.tileheight))
        positions.append(
            ((self.x + 15) / self.level.map.tilewidth, (self.y + 15 + self.speed) / self.level.map.tileheight))
        return positions

    def run(self):
        positions = []

        if not self.active:
            if self.respawn_counter > 0:
                self.respawn_counter -= 1

            if self.respawn_counter == 0:
                self.respawn = True

            if self.respawn:
                if self.anim_respawn.counter < 2:
                    self.anim_respawn.counter += 1
                else:
                    self.anim_respawn.counter = 0

                    if self.anim_respawn.active_frame < len(self.anim_respawn.frames) - 1:
                        self.anim_respawn.active_frame += 1
                    else:
                        self.init_enemy()

        if self.active:

            if self.shock_counter > 0:
                self.shock_counter -= 1

            if self.change_movement < 11:
                self.change_movement += 1

            if self.energy == 0:
                self.active = False
                self.sound_player.play_sample('exp')

            if self.move == Enemy.HORIZONTAL:
                if self.direction == 1:
                    positions = self.__get_collision_list('right')

                    for p in positions:
                        if self.level.is_hard(p[0], p[1]):
                            self.move = Enemy.VERTICAL

                            # if self.change_movement > 10:
                            '''
                            Start vertical movement, check for obstacles both at the top and at the bottom to decide
                            direction.
                            '''
                            bottom_obstacle_found = False
                            top_obstacle_found = False
                            vertical_positions = self.__get_collision_list('bottom')

                            for vp in vertical_positions:
                                if self.level.is_hard(vp[0], vp[1]):
                                    bottom_obstacle_found = True

                            vertical_positions = self.__get_collision_list('top')

                            for vp in vertical_positions:
                                if self.level.is_hard(vp[0], vp[1]):
                                    top_obstacle_found = True

                            if (top_obstacle_found and bottom_obstacle_found):
                                self.move = Enemy.HORIZONTAL
                                self.direction = -1
                                self.change_movement = 0
                            elif top_obstacle_found and not bottom_obstacle_found:
                                self.move = Enemy.VERTICAL
                                self.direction = 1
                                self.change_movement = 0
                            elif not top_obstacle_found and bottom_obstacle_found:
                                self.move = Enemy.VERTICAL
                                self.direction = -1
                                self.change_movement = 0
                            else:
                                self.move = Enemy.VERTICAL
                                self.direction = -1 if random.randint(0, 1) == 0 else 1
                                self.change_movement = 0
                            '''
                            else:
                                self.move = Enemy.HORIZONTAL
                                self.direction = -1
                                self.change_movement = 0
                            '''
                            self.move = Enemy.HORIZONTAL
                            self.direction = -1
                            self.change_movement = 0

                else:

                    positions = self.__get_collision_list('left')

                    for p in positions:
                        if self.level.is_hard(p[0], p[1]):
                            self.move = Enemy.VERTICAL

                            # if self.change_movement > 10:

                            '''
                            Start vertical movement, check for obstacles both at the top and at the bottom to decide
                            direction.
                            '''
                            bottom_obstacle_found = False
                            top_obstacle_found = False
                            vertical_positions = self.__get_collision_list('bottom')

                            for vp in vertical_positions:
                                if self.level.is_hard(vp[0], vp[1]):
                                    bottom_obstacle_found = True

                            vertical_positions = self.__get_collision_list('top')

                            for vp in vertical_positions:
                                if self.level.is_hard(vp[0], vp[1]):
                                    top_obstacle_found = True

                            if (top_obstacle_found and bottom_obstacle_found):
                                self.move = Enemy.HORIZONTAL
                                self.change_movement = 0
                                self.direction = 1
                            elif top_obstacle_found and not bottom_obstacle_found:
                                self.move = Enemy.VERTICAL
                                self.direction = 1
                                self.change_movement = 0
                            elif not top_obstacle_found and bottom_obstacle_found:
                                self.move = Enemy.VERTICAL
                                self.direction = -1
                                self.change_movement = 0
                            else:
                                self.move = Enemy.VERTICAL
                                self.direction = -1 if random.randint(0, 1) == 0 else 1
                                self.change_movement = 0
                            '''
                            else:
                                self.move = Enemy.HORIZONTAL
                                self.change_movement = 0
                                self.direction = 1
                            '''
                            self.move = Enemy.HORIZONTAL
                            self.change_movement = 0
                            self.direction = 1

                speed = self.speed

                if self.shock_counter > 0:
                    speed = 1

                self.x += (speed * self.direction)

            elif self.move == Enemy.VERTICAL:
                if self.direction == 1:

                    positions = self.__get_collision_list('bottom')

                    for p in positions:
                        if self.level.is_hard(p[0], p[1]):
                            self.move = Enemy.HORIZONTAL

                            # if self.change_movement > 10:
                            '''
                            Start horizontal movement, check for obstacles both at the left and at the right to decide
                            direction.
                            '''
                            left_obstacle_found = False
                            right_obstacle_found = False
                            horizontal_positions = self.__get_collision_list('left')

                            for hp in horizontal_positions:
                                if self.level.is_hard(hp[0], hp[1]):
                                    left_obstacle_found = True

                            horizontal_positions = self.__get_collision_list('right')
                            horizontal_positions.append(((self.x + 15 + self.speed) / self.level.map.tilewidth,
                                                         self.y / self.level.map.tileheight))
                            horizontal_positions.append(((self.x + 15 + self.speed) / self.level.map.tilewidth,
                                                         (self.y + 8) / self.level.map.tileheight))
                            horizontal_positions.append(((self.x + 15 + self.speed) / self.level.map.tilewidth,
                                                         (self.y + 15) / self.level.map.tileheight))

                            for hp in horizontal_positions:
                                if self.level.is_hard(hp[0], hp[1]):
                                    right_obstacle_found = True

                            if (left_obstacle_found and right_obstacle_found):
                                self.change_movement = 0
                                self.move = Enemy.VERTICAL
                                self.direction = -1
                            elif left_obstacle_found and not right_obstacle_found:
                                self.direction = 1
                                self.move = Enemy.HORIZONTAL
                                self.change_movement = 0
                            elif not left_obstacle_found and right_obstacle_found:
                                self.direction = -1
                                self.move = Enemy.HORIZONTAL
                                self.change_movement = 0
                            else:
                                self.direction = -1 if random.randint(0, 1) == 0 else 1
                                self.move = Enemy.HORIZONTAL
                                self.change_movement = 0
                            '''
                            else:
                                self.change_movement = 0
                                self.move = Enemy.VERTICAL
                                self.direction = -1
                            '''
                            self.change_movement = 0
                            self.move = Enemy.VERTICAL
                            self.direction = -1

                else:
                    positions = self.__get_collision_list('top')

                    for p in positions:
                        if self.level.is_hard(p[0], p[1]):
                            self.move = Enemy.HORIZONTAL

                            # if self.change_movement > 10:
                            '''
                            Start horizontal movement, check for obstacles both at the left and at the right to decide
                            direction.
                            '''
                            left_obstacle_found = False
                            right_obstacle_found = False
                            horizontal_positions = self.__get_collision_list('left')

                            for hp in horizontal_positions:
                                if self.level.is_hard(hp[0], hp[1]):
                                    left_obstacle_found = True

                            horizontal_positions = self.__get_collision_list('right')

                            for hp in horizontal_positions:
                                if self.level.is_hard(hp[0], hp[1]):
                                    right_obstacle_found = True

                            if (left_obstacle_found and right_obstacle_found):
                                self.change_movement = 0
                                self.move = Enemy.VERTICAL
                                self.direction = 1
                            elif left_obstacle_found and not right_obstacle_found:
                                self.direction = 1
                                self.move = Enemy.HORIZONTAL
                                self.change_movement = 0
                            elif not left_obstacle_found and right_obstacle_found:
                                self.direction = -1
                                self.move = Enemy.HORIZONTAL
                                self.change_movement = 0
                            else:
                                self.direction = -1 if random.randint(0, 1) == 0 else 1
                                self.change_movement = 0
                                self.move = Enemy.HORIZONTAL
                            '''
                            else:
                                self.change_movement = 0
                                self.move = Enemy.VERTICAL
                                self.direction = 1
                            '''
                            self.change_movement = 0
                            self.move = Enemy.VERTICAL
                            self.direction = 1

                speed = self.speed

                if self.shock_counter > 0:
                    speed = 1
                self.y += (speed * self.direction)

            if self.anim.counter < self.anim.frames[self.anim.active_frame].duration:
                self.anim.counter += 1
            else:
                self.anim.counter = 0

                if self.anim.active_frame < len(self.anim.frames) - 1:
                    self.anim.active_frame += 1
                else:
                    self.anim.active_frame = 0

            # Check if enemy hits the player
            self._hits_player()

    def _hits_player(self):
        player = PlayerUtils.get_player(self.game_context)

        if (self.x + self.size[0] + 256) >= (player.x - 8) and (self.x + 256) <= (player.x + 8) and (self.y + self.size[1] + 144) >= (player.y - 8) and (self.y + 144) <= (player.y + 8):
            player_crap_particles = PlayerUtils.get_particles_manager(self.game_context).get('crap')
            player_crap_particles.generate((player.x - 5, player.x + 2, player.y - 5, player.y + 2))
            player.life -= 1
            player.hit = True

    def render(self, screen):
        if self.active:
            if self.shock_counter > 0:
                screen.blit(self.anim_respawn.images['3'],
                            (self.x + 256 + self.anim_respawn.frames[3].offsetx,
                             self.y + 144 + self.anim_respawn.frames[3].offsety))
            else:
                screen.blit(self.anim.images[str(self.anim.active_frame)],
                            (self.x + 256 + self.anim.frames[self.anim.active_frame].offsetx,
                             self.y + 144 + self.anim.frames[self.anim.active_frame].offsety))

        if self.respawn:
            screen.blit(self.anim_respawn.images[str(self.anim_respawn.active_frame)],
                        (self.x + 256 + self.anim_respawn.frames[self.anim_respawn.active_frame].offsetx,
                         self.y + 144 + self.anim_respawn.frames[self.anim_respawn.active_frame].offsety))

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
            EnemyAnimations.animations[e + '_init'] = game_context.resourcemanager.get(e + '_init')


class PlayerUtils(object):
    @staticmethod
    def get_player(game_context):
        return game_context.player

    @staticmethod
    def get_particles_manager(game_context):
        return game_context.particlesmanager


class EnemyUtils(object):
    @staticmethod
    def get_nearby_enemies(enemies, position):
        result = []
        x = position[0] - 264
        y = position[1] - 152

        for e in enemies:
            if e.active:
                if (e.y < y + 16) and (e.y + e.size[1]) > y:
                    result.append(e)

        return result
