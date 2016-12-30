import math
import random
from gettext import gettext as _


class Enemy(object):
    HORIZONTAL = 0
    VERTICAL = 1
    DIAGONAL = 2

    def __init__(self, enemy_type, position, game_context):
        self._game_context = game_context
        self._level = game_context.current_level
        self._sound_player = game_context.sound_player
        self._x = position[0]
        self._y = position[1]
        self._enemy_type = enemy_type
        self._shock_counter = 0
        self._active = False
        self._animation = EnemyAnimations.animations[self._enemy_type]
        self._animation_respawn = EnemyAnimations.animations[self._enemy_type + '_init']
        self._size = self._animation.images[str(0)].get_size()
        self._init_enemy()

    '''
    Private methods
    '''

    def __cmp__(self, enemy):
        if self._x < enemy.x:
            return -1
        elif self._x > enemy.x:
            return 1
        else:
            return 0

    def __str__(self):
        return ''.join([str(self._enemy_type), ';', str(self._x), ';', str(self._y)])

    def _init_enemy(self):
        self._animation.active_frame = 0
        self._animation_respawn.active_frame = 0
        self._shock_counter = 0
        self._active = True
        self._change_movement = 0
        self._respawn = False
        self._respawn_counter = random.randint(50, 200)
        self._direction = 1
        self._speed = random.randint(1, 4)
        self._move = random.randint(0, 1)
        self._adjust_energy()

    def _adjust_energy(self):
        if self._enemy_type == 'jellyfish00':
            self.energy = 2
        elif self._enemy_type == 'devil00':
            self.energy = 2
        elif self._enemy_type == 'jellyfish01':
            self.energy = 3
        elif self._enemy_type == 'devil01':
            self.energy = 1

    def _get_collision_list(self, facing):
        if facing == 'left':
            return self._get_left_collision_list()
        elif facing == 'right':
            return self._get_right_collision_list()
        elif facing == 'top':
            return self._get_upper_collision_list()
        else:
            return self._get_bottom_collision_list()

    def _get_left_collision_list(self):
        positions = [
            ((self._x - self._speed) / self._level.map.tilewidth,
             self._y / self._level.map.tileheight),
            ((self._x - self._speed) / self._level.map.tilewidth,
             (self._y + 8) / self._level.map.tileheight),
            ((self._x - self._speed) / self._level.map.tilewidth,
             (self._y + 15) / self._level.map.tileheight)]
        return positions

    def _get_right_collision_list(self):
        positions = [
            ((self._x + 15 + self._speed) / self._level.map.tilewidth,
             self._y / self._level.map.tileheight),
            ((self._x + 15 + self._speed) / self._level.map.tilewidth,
             (self._y + 8) / self._level.map.tileheight),
            ((self._x + 15 + self._speed) / self._level.map.tilewidth,
             (self._y + 15) / self._level.map.tileheight)]
        return positions

    def _get_upper_collision_list(self):
        positions = [
            (self._x / self._level.map.tilewidth,
             (self._y - self._speed) / self._level.map.tileheight),
            ((self._x + 8) / self._level.map.tilewidth,
             (self._y - self._speed) / self._level.map.tileheight),
            ((self._x + 15) / self._level.map.tilewidth,
             (self._y - self._speed) / self._level.map.tileheight)]
        return positions

    def _get_bottom_collision_list(self):
        positions = [
            (self._x / self._level.map.tilewidth,
             (self._y + 15 + self._speed) / self._level.map.tileheight),
            ((self._x + 8) / self._level.map.tilewidth,
             (self._y + 15 + self._speed) / self._level.map.tileheight),
            ((self._x + 15) / self._level.map.tilewidth,
             (self._y + 15 + self._speed) / self._level.map.tileheight)]
        return positions

    def _run_hits_player(self):
        player = PlayerUtils.get_player(self._game_context)
        if not player.dying and not player.inmortal:
            if (self._x + self._size[0] + 256) >= (player.x - 8) \
                    and (self._x + 256) <= (player.x + 8) \
                    and (self._y + self._size[1] + 144) >= (player.y - 8) \
                    and (self._y + 144) <= (player.y + 8):
                crap_particles = PlayerUtils.get_particles_manager(self._game_context).get('crap')
                crap_particles.generate((player.x - 8, player.x + 5, player.y - 8, player.y + 5))
                player.hit = True
                self._sound_player.play_sample('player_hit_sam')

    def _run_respawn(self):
        if self._respawn_counter > 0:
            self._respawn_counter -= 1

        if self._respawn_counter == 0:
            self._respawn = True

        if self._respawn:
            if self._animation_respawn.counter < 2:
                self._animation_respawn.counter += 1
            else:
                self._animation_respawn.counter = 0

                if self._animation_respawn.active_frame < len(
                        self._animation_respawn.frames) - 1:
                    self._animation_respawn.active_frame += 1
                else:
                    self._init_enemy()

    def _run_shock(self):
        if self._shock_counter > 0:
            self._shock_counter -= 1

    def _run_horizontal_movement(self):
        if self._direction == 1:
            positions = self._get_collision_list('right')

            for p in positions:
                if self._level.is_hard(p[0], p[1]):
                    self._move = Enemy.VERTICAL
                    '''
                    Start vertical movement, check for obstacles both at the top and at the
                    bottom to decide direction.
                    '''
                    bottom_obstacle_found = False
                    top_obstacle_found = False
                    vertical_positions = self._get_collision_list('bottom')

                    for vp in vertical_positions:
                        if self._level.is_hard(vp[0], vp[1]):
                            bottom_obstacle_found = True

                    vertical_positions = self._get_collision_list('top')

                    for vp in vertical_positions:
                        if self._level.is_hard(vp[0], vp[1]):
                            top_obstacle_found = True

                    if top_obstacle_found and bottom_obstacle_found:
                        self._move = Enemy.HORIZONTAL
                        self._direction = -1
                        self._change_movement = 0
                    elif top_obstacle_found and not bottom_obstacle_found:
                        self._move = Enemy.VERTICAL
                        self._direction = 1
                        self._change_movement = 0
                    elif not top_obstacle_found and bottom_obstacle_found:
                        self._move = Enemy.VERTICAL
                        self._direction = -1
                        self._change_movement = 0
                    else:
                        self._move = Enemy.VERTICAL
                        self._direction = -1 if random.randint(0, 1) == 0 else 1
                        self._change_movement = 0
                    '''
                    else:
                        self.move = Enemy.HORIZONTAL
                        self.direction = -1
                        self.change_movement = 0
                    '''
                    self._move = Enemy.HORIZONTAL
                    self._direction = -1
                    self._change_movement = 0
        else:
            positions = self._get_collision_list('left')

            for p in positions:
                if self._level.is_hard(p[0], p[1]):
                    self._move = Enemy.VERTICAL

                    # if self.change_movement > 10:

                    '''
                    Start vertical movement, check for obstacles both at the top and at the
                    bottom to decide direction.
                    '''
                    bottom_obstacle_found = False
                    top_obstacle_found = False
                    vertical_positions = self._get_collision_list('bottom')

                    for vp in vertical_positions:
                        if self._level.is_hard(vp[0], vp[1]):
                            bottom_obstacle_found = True

                    vertical_positions = self._get_collision_list('top')

                    for vp in vertical_positions:
                        if self._level.is_hard(vp[0], vp[1]):
                            top_obstacle_found = True

                    if top_obstacle_found and bottom_obstacle_found:
                        self._move = Enemy.HORIZONTAL
                        self._change_movement = 0
                        self._direction = 1
                    elif top_obstacle_found and not bottom_obstacle_found:
                        self._move = Enemy.VERTICAL
                        self._direction = 1
                        self._change_movement = 0
                    elif not top_obstacle_found and bottom_obstacle_found:
                        self._move = Enemy.VERTICAL
                        self._direction = -1
                        self._change_movement = 0
                    else:
                        self._move = Enemy.VERTICAL
                        self._direction = -1 if random.randint(0, 1) == 0 else 1
                        self._change_movement = 0
                    '''
                    else:
                        self.move = Enemy.HORIZONTAL
                        self.change_movement = 0
                        self.direction = 1
                    '''
                    self._move = Enemy.HORIZONTAL
                    self._change_movement = 0
                    self._direction = 1

        speed = self._speed

        if self._shock_counter > 0:
            speed = 1

        self._x += (speed * self._direction)

    def _run_vertical_movement(self):
        if self._direction == 1:
            positions = self._get_collision_list('bottom')
            for p in positions:
                if self._level.is_hard(p[0], p[1]):
                    self._move = Enemy.HORIZONTAL

                    '''
                    Start horizontal movement, check for obstacles both at the left and at the
                    right to decide direction.
                    '''
                    left_obstacle_found = False
                    right_obstacle_found = False
                    horizontal_positions = self._get_collision_list('left')

                    for hp in horizontal_positions:
                        if self._level.is_hard(hp[0], hp[1]):
                            left_obstacle_found = True

                    horizontal_positions = self._get_collision_list('right')
                    horizontal_positions.append(
                        ((self._x + 15 + self._speed) / self._level.map.tilewidth,
                         self._y / self._level.map.tileheight))
                    horizontal_positions.append(
                        ((self._x + 15 + self._speed) / self._level.map.tilewidth,
                         (self._y + 8) / self._level.map.tileheight))
                    horizontal_positions.append(
                        ((self._x + 15 + self._speed) / self._level.map.tilewidth,
                         (self._y + 15) / self._level.map.tileheight))

                    for hp in horizontal_positions:
                        if self._level.is_hard(hp[0], hp[1]):
                            right_obstacle_found = True

                    if left_obstacle_found and right_obstacle_found:
                        self._change_movement = 0
                        self._move = Enemy.VERTICAL
                        self._direction = -1
                    elif left_obstacle_found and not right_obstacle_found:
                        self._direction = 1
                        self._move = Enemy.HORIZONTAL
                        self._change_movement = 0
                    elif not left_obstacle_found and right_obstacle_found:
                        self._direction = -1
                        self._move = Enemy.HORIZONTAL
                        self._change_movement = 0
                    else:
                        self._direction = -1 if random.randint(0, 1) == 0 else 1
                        self._move = Enemy.HORIZONTAL
                        self._change_movement = 0
                    '''
                    else:
                        self.change_movement = 0
                        self.move = Enemy.VERTICAL
                        self.direction = -1
                    '''
                    self._change_movement = 0
                    self._move = Enemy.VERTICAL
                    self._direction = -1

        else:
            positions = self._get_collision_list('top')

            for p in positions:
                if self._level.is_hard(p[0], p[1]):
                    self._move = Enemy.HORIZONTAL

                    # if self.change_movement > 10:
                    '''
                    Start horizontal movement, check for obstacles both at the left and at the
                    right to decide direction.
                    '''
                    left_obstacle_found = False
                    right_obstacle_found = False
                    horizontal_positions = self._get_collision_list('left')

                    for hp in horizontal_positions:
                        if self._level.is_hard(hp[0], hp[1]):
                            left_obstacle_found = True

                    horizontal_positions = self._get_collision_list('right')

                    for hp in horizontal_positions:
                        if self._level.is_hard(hp[0], hp[1]):
                            right_obstacle_found = True

                    if left_obstacle_found and right_obstacle_found:
                        self._change_movement = 0
                        self._move = Enemy.VERTICAL
                        self._direction = 1
                    elif left_obstacle_found and not right_obstacle_found:
                        self._direction = 1
                        self._move = Enemy.HORIZONTAL
                        self._change_movement = 0
                    elif not left_obstacle_found and right_obstacle_found:
                        self._direction = -1
                        self._move = Enemy.HORIZONTAL
                        self._change_movement = 0
                    else:
                        self._direction = -1 if random.randint(0, 1) == 0 else 1
                        self._change_movement = 0
                        self._move = Enemy.HORIZONTAL
                    '''
                    else:
                        self.change_movement = 0
                        self.move = Enemy.VERTICAL
                        self.direction = 1
                    '''
                    self._change_movement = 0
                    self._move = Enemy.VERTICAL
                    self._direction = 1

        speed = self._speed

        if self._shock_counter > 0:
            speed = 1
        self._y += (speed * self._direction)

    def _run_animation_frame(self):
        if self._animation.counter < self._animation.frames[self._animation.active_frame].duration:
            self._animation.counter += 1
        else:
            self._animation.counter = 0

            if self._animation.active_frame < len(self._animation.frames) - 1:
                self._animation.active_frame += 1
            else:
                self._animation.active_frame = 0

    '''
    Public methods
    '''

    def run(self):
        if not self._active:
            self._run_respawn()

        if self._active:
            self._run_shock()

            if self._change_movement < 11:
                self._change_movement += 1

            if self.energy == 0:
                self._active = False
                self._sound_player.play_sample('exp')

            if self._move == Enemy.HORIZONTAL:
                self._run_horizontal_movement()
            elif self._move == Enemy.VERTICAL:
                self._run_vertical_movement()

            self._run_animation_frame()
            self._run_hits_player()

    def render(self, screen):
        if self._active:
            if self._shock_counter > 0:
                screen.blit(self._animation_respawn.images['3'],
                            (self._x + 256 + self._animation_respawn.frames[3].offset_x,
                             self._y + 144 + self._animation_respawn.frames[3].offset_y))
            else:
                screen.blit(self._animation.images[str(self._animation.active_frame)],
                            (self._x + 256 + self._animation.frames[
                                self._animation.active_frame].offset_x,
                             self._y + 144 + self._animation.frames[
                                 self._animation.active_frame].offset_y))

        if self._respawn:
            screen.blit(self._animation_respawn.images[str(self._animation_respawn.active_frame)],
                        (self._x + 256 + self._animation_respawn.frames[
                            self._animation_respawn.active_frame].offset_x,
                         self._y + 144 + self._animation_respawn.frames[
                             self._animation_respawn.active_frame].offset_y))

    @property
    def active(self):
        return self._active

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def size(self):
        return self._size

    @property
    def shock_counter(self):
        return self._shock_counter

    @shock_counter.setter
    def shock_counter(self, value):
        self._shock_counter = value


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

            # Get total = 100%
            total = 0
            enemy_amount = {}
            for k, v in enemy_data.iteritems():
                if k in [''.join([e, '_frequency']) for e in EnemyBuilder.enemy_list]:
                    total += int(v)
                    enemy_amount[k] = math.floor((max_enemies * int(v)) / 100)

            # Build enemies
            # To calculate the initial position of the enemy in the map, we need enemy width and
            # height of the initial frame, (usually, all enemies frames will be of the same size)
            '''
            enemy_sizes = {enemy_name: anim_info.images['0'].get_size()
                           for enemy_name, anim_info in EnemyAnimations.animations.iteritems()}
            '''

            for k, v in enemy_amount.iteritems():
                for e in range(int(v)):
                    position = EnemyBuilder._get_initial_position(level)

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
    def _get_initial_position(level):

        # Calculate enemies initial position, check here that position doesn't overwrite
        # hard zones in the map information.

        found_hard_zones = True
        x, y = 0, 0

        while found_hard_zones:
            x = random.randint(0, level.map.width * level.map.tilewidth)
            y = random.randint(0, level.map.height * level.map.tileheight)

            positions = [
                (x / level.map.tilewidth, y / level.map.tileheight),
                ((x + 8) / level.map.tilewidth, y / level.map.tileheight),
                ((x + 15) / level.map.tilewidth, y / level.map.tileheight),
                (x / level.map.tilewidth, (y + 15) / level.map.tileheight),
                ((x + 8) / level.map.tilewidth, (y + 8) / level.map.tileheight),
                ((x + 15) / level.map.tilewidth, (y + 15) / level.map.tileheight)]

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
            EnemyAnimations.animations[e] = game_context.resource_manager.get(e)
            EnemyAnimations.animations[e + '_init'] = game_context.resource_manager.get(e + '_init')


class PlayerUtils(object):
    @staticmethod
    def get_player(game_context):
        return game_context.player

    @staticmethod
    def get_particles_manager(game_context):
        return game_context.particles_manager


class EnemyUtils(object):
    @staticmethod
    def get_nearby_enemies(enemies, position):
        result = []
        # x = position[0] - 264
        y = position[1] - 152

        for enemy in enemies:
            if enemy.active:
                if (enemy.y < y + 16) and (enemy.y + enemy.size[1]) > y:
                    result.append(enemy)

        return result
