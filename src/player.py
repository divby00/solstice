import enemy
import teleport
import info_area


class Laser(object):
    def __init__(self, laser_sprites, position, direction):
        self._active = True
        self._animation = 4
        self._direction = direction
        self._limit = [0, 0]
        self._position = position
        self._laser_sprites = laser_sprites

    '''
    Public methods
    '''

    def run(self):
        if self._animation > 0:
            self._animation -= 1

    def render(self, screen):
        if self._direction == 1:
            if self._animation >= 3:
                screen.blit(self._laser_sprites[0], (self._position[0], self._position[1]))
                for i in xrange(self._position[0] + 8, self._position[2], 4):
                    screen.blit(self._laser_sprites[3], (i, self._position[1]))
            if self._animation == 2:
                screen.blit(self._laser_sprites[1], (self._position[0], self._position[1]))
                for i in xrange(self._position[0] + 8, self._position[2], 4):
                    screen.blit(self._laser_sprites[4], (i, self._position[1]))
            if self._animation == 1:
                screen.blit(self._laser_sprites[2], (self._position[0], self._position[1]))
                for i in xrange(self._position[0] + 8, self._position[2], 4):
                    screen.blit(self._laser_sprites[5], (i, self._position[1]))
        else:
            if self._animation >= 3:
                screen.blit(self._laser_sprites[8], (self._position[0], self._position[1]))
                for i in xrange(self._position[0] - 4, self._position[2], -4):
                    screen.blit(self._laser_sprites[3], (i, self._position[1]))
            if self._animation == 2:
                screen.blit(self._laser_sprites[7], (self._position[0], self._position[1]))
                for i in xrange(self._position[0] - 4, self._position[2], -4):
                    screen.blit(self._laser_sprites[4], (i, self._position[1]))
            if self._animation == 1:
                screen.blit(self._laser_sprites[6], (self._position[0], self._position[1]))
                for i in xrange(self._position[0] - 4, self._position[2], -4):
                    screen.blit(self._laser_sprites[5], (i, self._position[1]))

    @property
    def animation(self):
        return self._animation


class Player(object):
    def __init__(self, context, game_context):
        self._x = 0
        self._y = 0
        self._w = 0
        self._h = 0
        self._thrust = 107
        self._bullets = 107
        self._life = 100
        self._lives = 3
        self._teleporting = False
        self._teleport_animation = -1
        self._destiny = None
        self._flying = False
        self._continuos_hit = 0
        self._using_item = False
        self._get_item_available = True
        self._get_item_counter = 5
        self._getting_item = False
        self._selected_item = None
        self._animation = 0
        self._recovery_mode = False
        self._recovery_animation = -1
        self._recovery_counter = 0
        self._direction = 0
        self._shoot_avail = True
        self._shoot_avail_counter = 0
        self._sprites = []
        self._sprites_hit = []
        self._recovery_spr = []
        self._teleport_spr = []
        self._sprites_inmortal = []
        self._laser_spr = []
        self._magnetic_fields = None
        self._info_areas = None
        self._nothrust = None
        self._rails = None
        self._container = None
        self._current_level = None
        self._sound_player = context.sound_player
        self._resource_manager = context.resource_manager
        self._particles_manager = context.particles_manager
        self._floor = game_context.scene_data if game_context.scene_data else 0
        self._teleports = None
        self._teleport_destiny = None
        self._teleport_source = None
        self._enemies = None
        self._firing = False
        self._hit = False
        self._dying = False
        self._respawn = False
        self._respawn_frame = 0
        self._inmortal = False
        self._active_info_area = None
        self._inmortal_frame = 0
        self._lasers = []
        self._init_sprites()

    '''
    Private methods
    '''

    def _init_sprites(self):
        self._sprites = [self._resource_manager.get('player' + str(index))
                         for index in xrange(0, 15)]
        self._sprites_hit = [self._resource_manager.get('player' + str(index) + '_hit')
                             for index in xrange(0, 15)]
        self._sprites_inmortal = [self._resource_manager.get('player' + str(index) + '_inmortal')
                                  for index in xrange(0, 15)]
        self._laser_spr = [self._resource_manager.get('shoot' + str(index))
                           for index in xrange(0, 9)]
        self._recovery_spr = [self._resource_manager.get('playerrecovery' + str(index))
                              for index in xrange(0, 4)]
        self._teleport_spr = [self._resource_manager.get('playerteleport' + str(index))
                              for index in xrange(0, 5)]

    def _run_status_falling(self):
        if not self._flying and not self._respawn:
            if not self._magnetic_fields:
                if not self.check_bottom_collision(self._current_level):
                    self._y += 4
                    return

            inside_magnetic_field = False

            for m in self._magnetic_fields:
                if self._x - 8 >= m.position[0] and self._x + 8 <= m.position[0] + m.size[0] \
                        and self._y - 8 >= m.position[1] \
                        and self._y + 8 <= m.position[1] + m.size[1]:
                    inside_magnetic_field = True

            if inside_magnetic_field and not self.check_upper_collision(self._current_level):
                self._y -= 4

            if not self.check_bottom_collision(self._current_level) and not inside_magnetic_field:
                self._y += 4

    def _run_status_info_area(self):
        for info in self._info_areas:
            if self._x + 8 >= info.position[0] and self._x - 8 <= info.position[0] + info.size[0] \
                    and self._y + 8 >= info.position[1] \
                    and self._y - 8 <= info.position[1] + info.size[1]:
                if self._active_info_area is None:
                    self._active_info_area = info_area.ActiveInfoArea(info.info_area_type,
                                                                      self._resource_manager)

    def _run_status_recovering(self):
        self._recovery_animation += 1
        self._life += .3

        if self._life >= 100:
            self._recovery_mode = False

        if self._recovery_animation == 4:
            self._recovery_animation = -1

    def _run_status_teleporting(self):
        self._teleport_animation += 1

        if self._teleport_animation >= 5:
            self._teleport_animation = -1
            self._teleporting = False
            self._teleport_source.status = teleport.Teleport.INACTIVE
            self._x = self._teleport_destiny.x + 8
            self._y = self._teleport_destiny.y + 8
            teleport_id = self._teleport_destiny.teleport_id

            for destiny in self._teleports:
                if teleport_id == destiny.teleport_id \
                        and destiny.x + 8 != self._x or destiny.y + 8 != self._y:
                    self._teleport_destiny = destiny

    def _run_status_normal(self):
        self._animation += self._direction

        if self._animation == 15:
            self._animation = 0
        if self._animation < 0:
            self._animation = 14

    def _run_status_hit(self):
        self._recovery_mode = False
        self._recovery_counter = 0
        self._hit = False
        self._continuos_hit += 1
        self._life -= 1

        if self._life <= 0 and not self._dying:
            self._dying = True
            player_exp_particles = self._particles_manager.get('exp')
            player_exp_particles.generate((self._x - 8, self._x + 8, self._y - 8, self._y + 8))
            self._sound_player.play_sample('exp')
            self._lives -= 1

            if self._lives == 0:
                # TODO: Do GameOver!!!
                pass
            else:
                self._respawn = True
                player_respawn_particles = self._particles_manager.get('respawn_part')
                player_respawn_particles.generate((self._x - 2, self._x, self._y - 2, self._y))

    def _run_status_respawn(self):
        if self._respawn:
            self._respawn_frame += 1
            if self._respawn_frame >= 50:
                self._respawn_frame = 0
                self._respawn = False
                self._inmortal = True
                self._inmortal_frame = 0
                self._life = 100
                self._dying = False

    def _run_status_inmortal(self):
        if self._inmortal:
            self._inmortal_frame += 1
            if self._inmortal_frame >= 100:
                self._inmortal = False
                self._inmortal_frame = 0

    def _run_status_using_item(self):
        if self._using_item:
            item = self._selected_item
            item.run()
            self._using_item = False

    def _run_status_shooting(self):
        if self._firing:
            self._shoot_avail = False
            if self._direction == 1:
                colision_x, colision_type, damaged_enemy = self.get_laser_right_collision()
                particle_coordinates = (self._x + 4 + colision_x, self._x + 12 + colision_x,
                                        self._y - 8, self._y)

                if 'wall' == colision_type:
                    beam_particles = self._particles_manager.get('hit')
                    beam_particles.generate(particle_coordinates)
                else:
                    if damaged_enemy is not None:
                        enemy_hit_particles = self._particles_manager.get('enemy_hit')
                        enemy_hit_particles.generate(particle_coordinates)
                        damaged_enemy.energy -= 1
                        self._sound_player.play_sample('enemy_hit_sam')

                        if damaged_enemy.energy <= 0:
                            enemy_death_particles = self._particles_manager.get('enemy_death')
                            enemy_death_particles.generate(particle_coordinates)
                        else:
                            damaged_enemy.shock_counter = 14

                laser_coordinates = (self._x + 8, self._y - 8, self._x + 8 + colision_x)
                laser = Laser(self._laser_spr, laser_coordinates, self._direction)

            else:
                colision_x, colision_type, damaged_enemy = self.get_laser_left_collision()
                particle_coordinates = (self._x - 20 - colision_x, self._x - 12 - colision_x,
                                        self._y - 8, self._y)

                if 'wall' == colision_type:
                    beam_particles = self._particles_manager.get('hit')
                    beam_particles.generate(particle_coordinates)
                else:
                    if damaged_enemy is not None:
                        enemy_hit_particles = self._particles_manager.get('enemy_hit')
                        enemy_hit_particles.generate(particle_coordinates)
                        damaged_enemy.energy -= 1
                        self._sound_player.play_sample('enemy_hit_sam')

                        if damaged_enemy.energy <= 0:
                            enemy_death_particles = self._particles_manager.get('enemy_death')
                            enemy_death_particles.generate(particle_coordinates)
                        else:
                            damaged_enemy.shock_counter = 14

                laser_coordinates = (self._x - 16, self._y - 8, self._x - 16 - colision_x)
                laser = Laser(self._laser_spr, laser_coordinates, self._direction)

            self._lasers.append(laser)
            self._firing = False

    def _run_lasers(self):
        for laser in self._lasers:
            laser.run()
            if laser.animation == 0:
                self._lasers.remove(laser)

    def _run_shoot_available(self):
        if not self._shoot_avail:
            self._shoot_avail_counter += 1
            if self._shoot_avail_counter == 4:
                self._shoot_avail = True
                self._shoot_avail_counter = 0

    '''
    Public methods
    '''

    def on_start(self, game_context):
        self._magnetic_fields = game_context.magnetic_fields
        self._info_areas = game_context.info_areas
        self._active_info_area = None
        self._nothrust = game_context.nothrust
        self._rails = game_context.rails
        self._container = game_context.container
        self._current_level = game_context.current_level
        self._teleports = game_context.teleports
        self._enemies = game_context.enemies
        self._w = self._sprites[0].get_width()
        self._h = self._sprites[0].get_height()
        self._x = ((self._current_level.start_point[0]) + 256 + 8)
        self._y = ((self._current_level.start_point[1]) + 144 + 8)
        self._animation = 0
        self._direction = 1
        self._teleporting = False
        self._teleport_animation = -1
        self._teleport_destiny = None
        self._teleport_source = None
        self._continuos_hit = 0
        self._firing = False
        self._hit = False
        self._dying = False
        self._respawn = False
        self._respawn_frame = 0
        self._inmortal = False
        self._inmortal_frame = 0
        self._lasers = []
        self._using_item = False
        self._flying = False
        self._thrust = 107
        self._bullets = 107
        self._life = 100
        self._selected_item = None
        self._get_item_counter = 5
        self._get_item_available = True
        self._getting_item = False
        self._recovery_mode = False
        self._recovery_animation = -1
        self._recovery_counter = 0
        self._shoot_avail = True
        self._shoot_avail_counter = 0

    def run(self):
        self._run_status_falling()

        if self._recovery_mode:
            self._run_status_recovering()
        elif self._teleporting:
            self._run_status_teleporting()
        else:
            self._run_status_normal()

        self._run_status_using_item()
        self._run_status_shooting()
        self._run_lasers()
        self._run_shoot_available()

        if self._hit:
            self._run_status_hit()
        else:
            if self._continuos_hit > 0:
                self._continuos_hit -= 1

        self._run_status_respawn()
        self._run_status_inmortal()
        self._run_status_info_area()

    def render(self, screen):
        if not self._dying:
            if not self._recovery_mode and not self._teleporting:
                if not self._hit and not self._inmortal:
                    screen.blit(self._sprites[self._animation], (self._x - 8, self._y - 8))
                elif self._hit and not self._inmortal:
                    screen.blit(self._sprites_hit[self._animation], (self._x - 8, self._y - 8))
                elif self._inmortal:
                    screen.blit(self._sprites_inmortal[self._animation], (self._x - 8, self._y - 8))

                for laser in self._lasers:
                    laser.render(screen)

            elif self._recovery_mode:
                screen.blit(self._recovery_spr[self._recovery_animation],
                            (self._x - 8 - 16, self._y - 8 - 16))

            elif self._teleporting:
                screen.blit(self._teleport_spr[self._teleport_animation],
                            (self._x - 8, self._y - 8))

        if self._respawn:
            if self._respawn_frame < 10:
                screen.blit(self._teleport_spr[4], (self._x - 8, self._y - 8))
            elif 10 <= self._respawn_frame <= 20:
                screen.blit(self._teleport_spr[3], (self._x - 8, self._y - 8))
            elif 20 <= self._respawn_frame <= 30:
                screen.blit(self._teleport_spr[2], (self._x - 8, self._y - 8))
            elif 30 <= self._respawn_frame <= 40:
                screen.blit(self._teleport_spr[1], (self._x - 8, self._y - 8))
            elif 40 <= self._respawn_frame <= 50:
                screen.blit(self._teleport_spr[0], (self._x - 8, self._y - 8))

    def get_laser_right_collision(self):
        enemies_in_sight = sorted(enemy.EnemyUtils.get_nearby_enemies(self._enemies,
                                                                      (self._x, self._y)))
        calculated_x = int((self._x - 8 + self._w) / self._current_level.map.tilewidth) - 32
        calculated_x_limit = int((self._x + self._w + 248) / self._current_level.map.tilewidth) - 32
        calculated_y = self._y / self._current_level.map.tileheight - 18
        damaged_enemy = None
        enemy_result = -1
        wall_result = -1

        for enemy_in_sight in enemies_in_sight:
            if enemy_in_sight.x > (self._x - (264 + 16)) \
                    and (enemy_in_sight.x + enemy_in_sight.size[0]) < (calculated_x_limit * 8):
                a = abs(((enemy_in_sight.x + 8) / 8) - calculated_x) * 8
                enemy_result = a
                damaged_enemy = enemy_in_sight
                break

        for x in xrange(calculated_x, calculated_x_limit):
            if self._current_level.is_hard(x, calculated_y):
                a = abs(x - calculated_x) * 8
                if self._x % 8 is not 0:
                    a -= 4
                wall_result = a
                break

        if enemy_result == -1:
            enemy_result = 256

        if wall_result == -1:
            wall_result = 256

        return (wall_result, 'wall', None) if wall_result < enemy_result else (
            enemy_result, 'enemy', damaged_enemy)

    def get_laser_left_collision(self):
        enemies_in_sight = sorted(
            enemy.EnemyUtils.get_nearby_enemies(self._enemies, (self._x, self._y)), reverse=True)
        calculated_x = int((self._x - 16) / self._current_level.map.tilewidth) - 32
        calculated_x_limit = int((self._x - 264) / self._current_level.map.tilewidth) - 32
        calculated_y = self._y / self._current_level.map.tileheight - 18
        damaged_enemy = None
        enemy_result = -1
        wall_result = -1

        for enemy_in_sight in enemies_in_sight:
            if (self._x - 264) > enemy_in_sight.x > (calculated_x_limit * 8):
                a = abs(((enemy_in_sight.x + 8) / 8) - calculated_x) * 8
                damaged_enemy = enemy_in_sight
                enemy_result = a
                break

        for x in xrange(calculated_x, calculated_x_limit, -1):
            if self._current_level.is_hard(x, calculated_y):
                a = abs(x - calculated_x) * 8
                if self._x % 8 is 0:
                    a -= 4
                wall_result = a
                break

        if enemy_result == -1:
            enemy_result = 256

        if wall_result == -1:
            wall_result = 256

        return (wall_result, 'wall', None) if wall_result < enemy_result else (
            enemy_result, 'enemy', damaged_enemy)

    def check_in_active_teleport(self):
        for telport in self._teleports:
            if telport.status != teleport.Teleport.INACTIVE \
                    and self._x + 8 >= telport.x \
                    and self._x - 8 <= telport.x + telport.w + 8 \
                    and self._y - 8 == telport.y:
                return True
        return False

    def check_in_nothrust(self):
        for m in self._nothrust:
            if self._x - 8 >= m.position[0] and self._x + 8 <= m.position[0] + m.size[0] \
                    and self._y - 8 <= m.position[1] + m.size[1] \
                    and self._y >= m.position[1]:
                return True
        return False

    def check_in_rails(self):
        for rail in self._rails:
            if self._x - 8 >= rail.position[0] \
                    and self._x + 8 <= rail.position[0] + rail.size[0] \
                    and self._y + 8 == rail.position[1]:
                return rail.direction
        return 0

    def check_upper_collision(self, level):
        calculated_y = int((self._y - 9) / level.map.tileheight) - 18
        calculated_x = [
            int((self._x - 8) / level.map.tilewidth) - 32,
            int(((self._x - 8) + ((self._w / 2) - 1)) / level.map.tilewidth) - 32,
            int(((self._x - 8) + (self._w - 1)) / level.map.tilewidth) - 32
        ]
        result = False
        for i in calculated_x:
            if self._current_level.is_hard(i, calculated_y):
                result = True
        return result

    def check_bottom_collision(self, level):
        calculated_y = int(((self._y - 8) + self._h) / level.map.tileheight) - 18
        calculated_x = [
            int((self._x - 8) / level.map.tilewidth) - 32,
            int(((self._x - 8) + ((self._w / 2) - 1)) / level.map.tilewidth) - 32,
            int(((self._x - 8) + (self._w - 1)) / level.map.tilewidth) - 32
        ]
        result = False
        for i in calculated_x:
            if self._current_level.is_hard(i, calculated_y):
                result = True
        return result

    def check_right_collision(self, level):
        calculated_x = int(((self._x - 8) + self._w) / level.map.tilewidth) - 32
        calculated_y = [
            int((self._y - 8) / level.map.tilewidth) - 18,
            int(((self._y - 8) + ((self._h / 2) - 1)) / level.map.tilewidth) - 18,
            int(((self._y - 8) + (self._h - 1)) / level.map.tilewidth) - 18
        ]
        result = False
        for a in calculated_y:
            if self._current_level.is_hard(calculated_x, a):
                result = True
        return result

    def check_left_collision(self, level):
        calculated_x = int((self._x - 9) / level.map.tilewidth) - 32
        calculated_y = [
            int(self._y - 8 / level.map.tileheight) - 18,
            int((self._y - 8 + ((self._h / 2) - 1)) / level.map.tileheight) - 18,
            int((self._y - 8 + (self._h - 1)) / level.map.tileheight) - 18
        ]
        result = False
        for a in calculated_y:
            if self._current_level.is_hard(calculated_x, a):
                result = True
        return result

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
    def continuos_hit(self):
        return self._continuos_hit

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, value):
        self._life = value

    @property
    def lives(self):
        return self._lives

    @property
    def thrust(self):
        return self._thrust

    @thrust.setter
    def thrust(self, value):
        self._thrust = value

    @property
    def bullets(self):
        return self._bullets

    @bullets.setter
    def bullets(self, value):
        self._bullets = value

    @property
    def selected_item(self):
        return self._selected_item

    @selected_item.setter
    def selected_item(self, value):
        self._selected_item = value

    @property
    def dying(self):
        return self._dying

    @dying.setter
    def dying(self, value):
        self._dying = value

    @property
    def inmortal(self):
        return self._inmortal

    @property
    def hit(self):
        return self._hit

    @hit.setter
    def hit(self, value):
        self._hit = value

    @property
    def teleport_source(self):
        return self._teleport_source

    @teleport_source.setter
    def teleport_source(self, value):
        self._teleport_source = value

    @property
    def teleport_destiny(self):
        return self._teleport_destiny

    @teleport_destiny.setter
    def teleport_destiny(self, value):
        self._teleport_destiny = value

    @property
    def get_item_counter(self):
        return self._get_item_counter

    @get_item_counter.setter
    def get_item_counter(self, value):
        self._get_item_counter = value

    @property
    def get_item_available(self):
        return self._get_item_available

    @get_item_available.setter
    def get_item_available(self, value):
        self._get_item_available = value

    @property
    def recovery_mode(self):
        return self._recovery_mode

    @recovery_mode.setter
    def recovery_mode(self, value):
        self._recovery_mode = value

    @property
    def recovery_counter(self):
        return self._recovery_counter

    @recovery_counter.setter
    def recovery_counter(self, value):
        self._recovery_counter = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    @property
    def flying(self):
        return self._flying

    @flying.setter
    def flying(self, value):
        self._flying = value

    @property
    def teleporting(self):
        return self._teleporting

    @teleporting.setter
    def teleporting(self, value):
        self._teleporting = value

    @property
    def shoot_avail(self):
        return self._shoot_avail

    @shoot_avail.setter
    def shoot_avail(self, value):
        self._shoot_avail = value

    @property
    def firing(self):
        return self._firing

    @firing.setter
    def firing(self, value):
        self._firing = value

    @property
    def using_item(self):
        return self._using_item

    @using_item.setter
    def using_item(self, value):
        self._using_item = value

    @property
    def continuos_hit(self):
        return self._continuos_hit

    @continuos_hit.setter
    def continuos_hit(self, value):
        self._continuos_hit = value

    @property
    def floor(self):
        return self._floor

    @floor.setter
    def floor(self, value):
        self._floor = value

    @property
    def active_info_area(self):
        return self._active_info_area

    @active_info_area.setter
    def active_info_area(self, value):
        self._active_info_area = value
