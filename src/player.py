import actor
import teleport
import enemy


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
    def __init__(self, context, game_context):
        super(Player, self).__init__(context)
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.thrust = 107
        self.bullets = 107
        self.life = 1
        self.lives = 3
        self.teleporting = False
        self.teleport_animation = -1
        self.destiny = None
        self.flying = False
        self.using_item = False
        self.get_item_available = True
        self.get_item_counter = 5
        self.getting_item = False
        self.selected_item = None
        self.animation = 0
        self.recovery_mode = False
        self.recovery_animation = -1
        self.recovery_counter = 0
        self.direction = 0
        self.shoot_avail = True
        self.shoot_avail_counter = 0
        self.sprites = []
        self.sprites_hit = []
        self.recovery_spr = []
        self.teleport_spr = []
        self.sprites_inmortal = []
        self.laser_spr = []
        self.magnetic_fields = None
        self.current_level = None
        self.sound_player = context.sound_player
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

        for p in xrange(0, len(player)):
            self.sprites_hit.insert(p, self.context.resourcemanager.get(''.join([player[p], '_hit'])))

        for p in xrange(0, len(player)):
            self.sprites_inmortal.insert(p, self.context.resourcemanager.get(''.join([player[p], '_inmortal'])))

        for l in xrange(0, len(laser)):
            self.laser_spr.insert(l, self.context.resourcemanager.get(laser[l]))

        for r in xrange(0, 4):
            self.recovery_spr.insert(r, self.context.resourcemanager.get('playerrecovery' + str(r)))

        for r in xrange(0, 5):
            self.teleport_spr.insert(r, self.context.resourcemanager.get('playerteleport' + str(r)))

        self.context.laser_spr = self.laser_spr

    def on_start(self, game_context):
        self.magnetic_fields = game_context.magnetic_fields
        self.current_level = game_context.current_level
        self.teleports = game_context.teleports
        self.enemies = game_context.enemies
        self.w = self.sprites[0].get_width()
        self.h = self.sprites[0].get_height()
        self.x = ((self.current_level.start_point[0]) + 256 + 8)
        self.y = ((self.current_level.start_point[1]) + 144 + 8)
        self.animation = 0
        self.direction = 1
        self.teleporting = False
        self.teleport_animation = -1
        self.destiny = None
        self.firing = False
        self.hit = False
        self.continuos_hit = 0
        self.dying = False
        self.respawn = False
        self.respawn_frame = 0
        self.inmortal = False
        self.inmortal_frame = 0
        self.using_item = False
        self.flying = False
        self.lasers = []
        self.thrust = 107
        self.bullets = 107
        self.life = 1
        self.lives = 3
        self.selected_item = None
        self.get_item_counter = 5
        self.get_item_available = True
        self.getting_item = False
        self.recovery_mode = False
        self.recovery_animation = -1
        self.recovery_counter = 0
        self.shoot_avail = True
        self.shoot_avail_counter = 0

    def run(self):
        if not self.flying:
            self.__goes_down()

        if self.recovery_mode:
            self.recovery_animation += 1
            self.life += .3

            if self.life >= 100:
                self.recovery_mode = False

            if self.recovery_animation == 4:
                self.recovery_animation = -1
        elif self.teleporting:
            self.teleport_animation += 1

            if self.teleport_animation >= 5:
                self.teleport_animation = -1
                self.teleporting = False
                self.x = self.destiny.x + 8
                self.y = self.destiny.y + 8
                id = self.destiny.id

                for destiny in self.teleports:
                    if id == destiny.id and destiny.x + 8 != self.x or destiny.y + 8 != self.y:
                        self.destiny = destiny
        else:
            self.animation += self.direction

            if self.animation == 15:
                self.animation = 0
            if self.animation < 0:
                self.animation = 14

        if self.using_item:
            self.use_item()
            self.using_item = False

        if self.firing:
            self.shoot()
            self.firing = False

        for l in self.lasers:
            l.run()

            if l.animation == 0:
                self.lasers.remove(l)

        if not self.shoot_avail:
            self.shoot_avail_counter += 1

            if self.shoot_avail_counter == 4:
                self.shoot_avail = True
                self.shoot_avail_counter = 0

        if self.hit:
            self.recovery_mode = False
            self.recovery_counter = 0
            self.hit = False
            self.continuos_hit += 1
            self.life -= 1

            if self.life <= 0 and self.dying == False:
                self.dying = True
                player_exp_particles = self.particlesmanager.get('exp')
                player_exp_particles.generate((self.x - 8, self.x + 8, self.y - 8, self.y + 8))
                self.sound_player.play_sample('exp')
                self.lives -= 1

                if self.lives == 0:
                    # TODO: Do GameOver!!!
                    pass
                else:
                    self.respawn = True
                    player_respawn_particles = self.particlesmanager.get('respawn_part')
                    player_respawn_particles.generate((self.x - 2, self.x, self.y - 2, self.y))
        else:
            if self.continuos_hit > 0:
                self.continuos_hit -= 1

        if self.respawn:
            self.respawn_frame += 1

            if self.respawn_frame >= 50:
                self.respawn_frame = 0
                self.respawn  = False
                self.inmortal = True
                self.inmortal_frame = 0
                self.life = 100
                self.dying = False

        if self.inmortal:
            self.inmortal_frame += 1

            if self.inmortal_frame >= 100:
                self.inmortal = False
                self.inmortal_frame = 0


    def render(self, screen):
        if not self.dying:
            if not self.recovery_mode and not self.teleporting:
                if not self.hit and not self.inmortal:
                    screen.blit(self.sprites[self.animation], (self.x - 8, self.y - 8))
                elif self.hit and not self.inmortal:
                    screen.blit(self.sprites_hit[self.animation], (self.x - 8, self.y - 8))
                elif self.inmortal:
                    screen.blit(self.sprites_inmortal[self.animation], (self.x - 8, self.y - 8))
                for l in self.lasers:
                    l.render(screen)
            elif self.recovery_mode:
                screen.blit(self.recovery_spr[self.recovery_animation], (self.x - 8 - 16, self.y - 8 - 16))
            elif self.teleporting:
                screen.blit(self.teleport_spr[self.teleport_animation], (self.x - 8, self.y - 8))

        if self.respawn:
            if self.respawn_frame < 10:
                screen.blit(self.teleport_spr[4], (self.x - 8, self.y - 8))
            elif self.respawn_frame >= 10 and self.respawn_frame <= 20:
                screen.blit(self.teleport_spr[3], (self.x - 8, self.y - 8))
            elif self.respawn_frame >= 20 and self.respawn_frame <= 30:
                screen.blit(self.teleport_spr[2], (self.x - 8, self.y - 8))
            elif self.respawn_frame >= 30 and self.respawn_frame <= 40:
                screen.blit(self.teleport_spr[1], (self.x - 8, self.y - 8))
            elif self.respawn_frame >= 40 and self.respawn_frame <= 50:
                screen.blit(self.teleport_spr[0], (self.x - 8, self.y - 8))

    def use_item(self):
        item = self.selected_item
        item.run()

    def shoot(self):
        laser = None
        self.shoot_avail = False
        if self.direction == 1:
            colision_x, colision_type, damaged_enemy = self.get_laser_right_collision()
            if 'wall' == colision_type:
                beam_particles = self.particlesmanager.get('hit')
                beam_particles.generate((self.x + 4 + colision_x, self.x + 12 + colision_x, self.y - 8, self.y))
            else:
                if damaged_enemy is not None:
                    enemy_hit_particles = self.particlesmanager.get('enemy_hit')
                    enemy_hit_particles.generate(
                        (self.x + 4 + colision_x, self.x + 12 + colision_x, self.y - 8, self.y))
                    damaged_enemy.energy -= 1
                    self.sound_player.play_sample('enemy_hit_sam')

                    if damaged_enemy.energy <= 0:
                        enemy_death_particles = self.particlesmanager.get('enemy_death')
                        enemy_death_particles.generate(
                            (self.x + 4 + colision_x, self.x + 12 + colision_x, self.y - 8, self.y))
                        # damaged_enemy.active = False
                    else:
                        damaged_enemy.shock_counter = 14

            laser = Laser(self.context, (self.x + 8, self.y - 8, self.x + 8 + colision_x), self.direction)
        else:
            colision_x, colision_type, damaged_enemy = self.get_laser_left_collision()

            if 'wall' == colision_type:
                beam_particles = self.particlesmanager.get('hit')
                beam_particles.generate((self.x - 20 - colision_x, self.x - 12 - colision_x, self.y - 8, self.y))
            else:
                if damaged_enemy is not None:
                    enemy_hit_particles = self.particlesmanager.get('enemy_hit')
                    enemy_hit_particles.generate(
                        (self.x - 20 - colision_x, self.x - 12 - colision_x, self.y - 8, self.y))
                    damaged_enemy.energy -= 1
                    self.sound_player.play_sample('enemy_hit_sam')

                    if damaged_enemy.energy <= 0:
                        enemy_death_particles = self.particlesmanager.get('enemy_death')
                        enemy_death_particles.generate(
                            (self.x - 20 - colision_x, self.x - 12 - colision_x, self.y - 8, self.y))
                        #damaged_enemy.active = False
                    else:
                        damaged_enemy.shock_counter = 14

            laser = Laser(self.context, (self.x - 16, self.y - 8, self.x - 16 - colision_x), self.direction)

        self.lasers.append(laser)

    def get_laser_right_collision(self):
        # TODO: Please check this 'optimization', do we really need to iterate through all the layers??
        # I have removed this loop from both player and laser collisions
        '''
        for l in self.current_level.layers:
            if l.name == 'hard':
        '''
        enemies_in_sight = sorted(enemy.EnemyUtils.get_nearby_enemies(self.enemies, (self.x, self.y)))
        calculated_x = int((self.x - 8 + self.w) / self.current_level.map.tilewidth) - 32
        calculated_x_limit = int((self.x + self.w + 248) / self.current_level.map.tilewidth) - 32
        calculated_y = self.y / self.current_level.map.tileheight - 18

        damaged_enemy = None
        enemy_result = -1
        wall_result = -1

        for e in enemies_in_sight:
            if (e.x > (self.x - (264 + 16)) and (e.x + e.size[0]) < (calculated_x_limit * 8)):
                a = abs(((e.x + 8) / 8) - calculated_x) * 8
                enemy_result = a
                damaged_enemy = e
                break

        for x in xrange(calculated_x, calculated_x_limit):
            if self.current_level.is_hard(x, calculated_y):
                a = abs(x - calculated_x) * 8
                if self.x % 8 is not 0:
                    a -= 4
                wall_result = a
                break

        if enemy_result == -1:
            enemy_result = 256

        if wall_result == -1:
            wall_result = 256

        return (wall_result, 'wall', None) if wall_result < enemy_result else (enemy_result, 'enemy', damaged_enemy)

    def get_laser_left_collision(self):
        enemies_in_sight = sorted(enemy.EnemyUtils.get_nearby_enemies(self.enemies, (self.x, self.y)), reverse=True)
        calculated_x = int((self.x - 16) / self.current_level.map.tilewidth) - 32
        calculated_x_limit = int((self.x - 264) / self.current_level.map.tilewidth) - 32
        calculated_y = self.y / self.current_level.map.tileheight - 18

        damaged_enemy = None
        enemy_result = -1
        wall_result = -1

        for e in enemies_in_sight:
            if (e.x < (self.x - 264) and e.x > (calculated_x_limit * 8)):
                a = abs(((e.x + 8) / 8) - calculated_x) * 8
                damaged_enemy = e
                enemy_result = a
                break

        for x in xrange(calculated_x, calculated_x_limit, -1):
            if self.current_level.is_hard(x, calculated_y):
                a = abs(x - calculated_x) * 8
                if self.x % 8 is 0:
                    a -= 4
                wall_result = a
                break

        if enemy_result == -1:
            enemy_result = 256

        if wall_result == -1:
            wall_result = 256

        return (wall_result, 'wall', None) if wall_result < enemy_result else (enemy_result, 'enemy', damaged_enemy)

    def __goes_down(self):
        for m in self.magnetic_fields:

            if self.x - 8 >= m.position[0] and self.x + 8 <= m.position[0] + m.size[0] and \
                                    self.y - 8 >= m.position[1] and self.y + 8 <= m.position[1] + m.size[1]:

                if not self.check_upper_collision(self.current_level):
                    self.y -= 4
            else:

                if not self.check_bottom_collision(self.current_level):
                    self.y += 4

    def check_in_active_teleport(self, level):
        for t in self.teleports:
            if t.status != teleport.Teleport.INACTIVE \
                    and self.x + 8 >= t.x and self.x - 8 <= t.x + t.w + 8 and self.y - 8 == t.y:
                return True
        return False

    def check_right_collision(self, level):
        calculated_x = int(((self.x - 8) + self.w) / level.map.tilewidth) - 32
        calculated_y = []
        calculated_y.insert(0, int((self.y - 8) / level.map.tilewidth) - 18)
        calculated_y.insert(1, int(((self.y - 8) + ((self.h / 2) - 1)) /
                                   level.map.tilewidth) - 18)
        calculated_y.insert(2, int(((self.y - 8) + (self.h - 1)) /
                                   level.map.tilewidth) - 18)
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
        result = False

        for i in calculated_x:
            if self.current_level.is_hard(i, calculated_y):
                result = True

        return result

    def check_bottom_collision(self, level):

        calculated_y = int(((self.y - 8) + self.h) / level.map.tileheight) - 18
        calculated_x = []
        calculated_x.insert(0, int((self.x - 8) / level.map.tilewidth) - 32)
        calculated_x.insert(1, int(((self.x - 8) + ((self.w / 2) - 1)) /
                                   level.map.tilewidth) - 32)
        calculated_x.insert(2, int(((self.x - 8) + (self.w - 1)) /
                                   level.map.tilewidth) - 32)
        result = False

        for i in calculated_x:
            if self.current_level.is_hard(i, calculated_y):
                result = True

        return result
