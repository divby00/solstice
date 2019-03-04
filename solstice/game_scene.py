import board
import container
import control
import enemy
import info_area
import item
import magnetic
import nothrust
import particles
import particles_manager
import player
import powerups
import rails
import renderer
import scene
import teleport
from life_exchanger import LifeExchangerBuilder
from crusher import CrusherBuilder
from lock import BeamBarriersBuilder, LockBuilder


class GameScene(scene.Scene):
    def __init__(self, context, name='game', scene_speed=33):
        super(GameScene, self).__init__(context, name, scene_speed)
        self._screen = context.screen
        self._locks = None
        self._life_exchangers = None
        self._beam_barriers = None
        self._items = None
        self._teleports = None
        self._magnetic_fields = None
        self._nothrust = None
        self._rails = None
        self._container = None
        self._enemies = None
        self._level = context.resource_manager.get('level00')
        self._current_level = None
        self._renderer_object = None
        self._enemies_renderer = None
        self._exit_point = None
        self._info_areas = None
        self._on_elevator = False
        self._powerups = None
        self._crushers = None
        self._particles_manager = GameScene._init_particles(context.resource_manager)
        context.particles_manager = self._particles_manager
        self._player = player.Player(context, self)
        self._board = board.Board(context, self._player)
        self._animations = context.resource_manager.animations
        self._resource_manager = context.resource_manager
        self._sound_player = context.sound_player
        self._sound_player.load_sample([
            'laser', 'accept', 'cancel', 'bulletsup', 'thrustup', 'exp', 'level01_song',
            'enemy_hit_sam', 'player_hit_sam', 'teleport', 'secured', 'ding', 'powerup'
        ])
        self.get_menu()

    '''
    Private methods
    '''

    @staticmethod
    def _init_particles(resource_manager):
        enemy_beam_particles = particles.EnemyBeamParticles(resource_manager, 'enemy_hit')
        beam_particles = particles.BeamParticles(resource_manager, 'hit')
        enemy_death_particles = particles.EnemyExplosionParticles(resource_manager, 'enemy_death')
        exp_particles = particles.ExplosionParticles(resource_manager, 'exp')
        player_crap_particles = particles.PlayerCrapParticles(resource_manager, 'crap')
        player_smoke_particles = particles.PlayerSmokeParticles(resource_manager, 'thrust')
        respawn_particles = particles.RespawnParticles(resource_manager, 'respawn_part')
        life_exchanger_particles = particles.LifeExchangerParticles(resource_manager, 'life_exchanger')
        particles_mngr = particles_manager.ParticlesManager()
        particles_mngr.register_particles(beam_particles)
        particles_mngr.register_particles(exp_particles)
        particles_mngr.register_particles(enemy_beam_particles)
        particles_mngr.register_particles(enemy_death_particles)
        particles_mngr.register_particles(player_crap_particles)
        particles_mngr.register_particles(player_smoke_particles)
        particles_mngr.register_particles(respawn_particles)
        particles_mngr.register_particles(life_exchanger_particles)
        return particles_mngr

    def _check_player_is_in_elevator(self):
        return self._player.x + 8 >= self._exit_point[0] \
               and self._player.x - 8 <= self._exit_point[0] + self._exit_point[2] \
               and self._player.y - 8 <= self._exit_point[1] + self._exit_point[3] \
               and self._player.y + 8 >= self._exit_point[1]

    def _run_powerups(self):
        self._powerups.run()

    def _run_info_areas(self):
        if self._player.active_info_area:
            running = self._player.active_info_area.run()
            if not running:
                self._player.active_info_area = None

    def _run_rails(self):
        rail_direction = self._player.check_in_rails()
        if rail_direction != 0:
            if not self._player.check_right_collision(self._current_level) and rail_direction == 1:
                self._player.x += self._renderer_object.speed[0]
            if not self._player.check_left_collision(self._current_level) and rail_direction == -1:
                self._player.x -= self._renderer_object.speed[0]

    def _run_menu_group(self):
        self._control.keyboard_event = self.keyboard_event
        self._control.event_driven = True
        self._menu_group.run()

    def _run_item_counter(self):
        if self._player.get_item_counter < 5:
            self._player.get_item_counter += 1

            if self._player.get_item_counter == 5:
                self._player.get_item_available = True

    def _run_recovery_counter(self):
        if not self._player.recovery_mode and self._player.life < 100:

            if self._player.recovery_counter < 100:
                self._player.recovery_counter += 1

            if self._player.recovery_counter == 100:
                self._player.recovery_mode = True

    def _run_control_right(self):
        self._player.recovery_counter = 0
        self._player.recovery_mode = False
        self._player.direction = 1

        if not self._player.check_right_collision(self._current_level) \
                and self._player.check_in_rails() == 0:
            self._player.x += self._renderer_object.speed[0]

    def _run_control_left(self):
        self._player.recovery_counter = 0
        self._player.recovery_mode = False
        self._player.direction = -1

        if not self._player.check_left_collision(self._current_level) \
                and self._player.check_in_rails() == 0:
            self._player.x -= self._renderer_object.speed[0]

    def _run_control_up(self):
        self._player.recovery_counter = 0
        self._player.recovery_mode = False
        self._player.thrust -= .1
        self._player.flying = True
        player_smoke_particles = self._particles_manager.get('thrust')
        player_smoke_particles.generate(
            (self._player.x - 4, self._player.x + 1, self._player.y + 6,
             self._player.y + 7))

        if not self._player.check_upper_collision(self._current_level) \
                and not self._player.check_in_nothrust():
            self._player.y -= self._renderer_object.speed[1]

            # Check if player is in teleport
            if self._player.check_in_active_teleport():
                self._player.teleporting = True
                self._sound_player.play_sample('teleport')

    def _run_control_down(self):
        self._player.recovery_mode = False
        self._player.recovery_counter = 0

        # Checks if player is over an item
        if self._player.get_item_available:
            x = self._player.x
            y = self._player.y

            for i in self._items:
                if x + 8 >= i.x and x - 8 <= i.x + i.w and y + 8 >= i.y and y - 8 <= i.y + i.h:
                    # Player is over an item
                    self._player.get_item_available = False
                    self._player.get_item_counter = 0
                    self._sound_player.play_sample('accept')

                    if not self._player.selected_item:
                        self._player.selected_item = i
                        self._items.remove(i)
                        self._renderer_object.change_animation((i.x, i.y), None)
                    else:
                        tmp_item = self._player.selected_item
                        x, y = i.x, i.y
                        self._player.selected_item = i
                        self._items.remove(i)
                        tmp_item.x, tmp_item.y = x, y
                        self._items.append(tmp_item)
                        self._renderer_object.change_animation((i.x, i.y), tmp_item.name)
                        break

    def _run_control_action1(self):
        if self._check_player_is_in_elevator():
            self._on_elevator = True

        if self._player.shoot_avail and self._player.bullets > 0:
            self._player.recovery_counter = 0
            self._player.recovery_mode = False
            self._sound_player.play_sample('laser')
            self._player.firing = True
            self._player.bullets -= .3

    def _run_control_action2(self):
        self._player.recovery_counter = 0
        self._player.recovery_mode = False

        if self._player.over_life_exchanger:
            life_ex_coordinates = self._player.life_exchanger_coordinates
            self._player.life = self._player.life - 100
            self._player.hit = True
            self._renderer_object.set_animation(life_ex_coordinates, 'teleport_pass')
            teleport_item = item.ItemTeleport(self, life_ex_coordinates, (16, 16))
            teleport_item._sprite = self._resource_manager.get('item_teleport_pass')
            self._items.append(teleport_item)

        if self._player.selected_item is not None:
            self._player.using_item = True
            self._sound_player.play_sample('accept')

    '''
    Public methods
    '''

    def on_start(self):
        self._on_elevator = False
        self.menu_group.visible = False
        # If the scene is set from elevator scene, scene_data will contain the selected floor
        if self._scene_data:
            self._level = self._resource_manager.get('level0' + str(self._scene_data + 1))
        self._current_level = self._level
        self._exit_point = self._level.exit_point[0] + 256, self._level.exit_point[1] + 144, \
                           self._level.exit_point[2], self._level.exit_point[3]
        self._enemies_renderer = enemy.EnemyAnimations.init(self)
        self._info_areas = info_area.InfoAreaBuilder.build(self._current_level.info_areas)
        self._magnetic_fields = magnetic.MagneticBuilder.build(self._current_level.magnetic_fields)
        self._nothrust = nothrust.NoThrustBuilder.build(self._current_level.nothrust)
        self._rails = rails.RailsBuilder.build(self._current_level.rails)
        self._container = container.ContainerBuilder.build(self._current_level.container_info)
        self._teleports = teleport.TeleportBuilder.build(self._current_level.teleports)
        self._locks = LockBuilder.build(self, self._current_level.locks)
        self._life_exchangers = LifeExchangerBuilder.build(self._current_level.life_exchangers)
        self._crushers = CrusherBuilder.build(self._current_level.crushers)
        self._beam_barriers = BeamBarriersBuilder.build(self._current_level.beam_barriers)
        self._enemies = enemy.EnemyBuilder.build(self)
        self._powerups = powerups.Powerups(self._player)
        self._player.on_start(self)
        self._renderer_object = renderer.Renderer(self)
        self._items = item.ItemBuilder.build(self, self._resource_manager,
                                             self._current_level.items)
        self._sound_player.play_sample('level01_song')
        self._control.event_driven = False

    def get_renderer(self):
        return self._renderer_object

    def get_layers(self):
        return self._current_level.layers

    def on_quit(self):
        self._sound_player.stop()

    def run(self):
        if self._on_elevator:
            self.enter_elevator(self._player)

        if self._menu_group.visible:
            self._run_menu_group()
        else:
            self._control.event_driven = False
            if not self._player.dying:
                self._player.flying = False
                self._run_item_counter()
                self._run_recovery_counter()

                if self._control.on(control.Control.RIGHT):
                    self._run_control_right()

                if self._control.on(control.Control.LEFT):
                    self._run_control_left()

                self._run_rails()

                if self._control.on(control.Control.UP) and self._player.thrust > 0:
                    self._run_control_up()

                if self._control.on(control.Control.DOWN):
                    self._run_control_down()

                if self._control.on(control.Control.ACTION1) and not self._player.teleporting:
                    self._run_control_action1()

                if self._control.on(control.Control.ACTION2) and not self._player.teleporting:
                    self._run_control_action2()

            if self._control.on(control.Control.START):
                self.menu_group.visible = True

            self._player.run()
            for the_enemy in self._enemies:
                the_enemy.run()
            self._run_powerups()
            self._run_info_areas()
            self._particles_manager.run()
            self._renderer_object.run()

    def render(self, screen):
        self._renderer_object.render()
        if self._menu_group.visible:
            self._menu_group.render(screen.virt, (128, 70))

    @property
    def resource_manager(self):
        return self._resource_manager

    @property
    def current_level(self):
        return self._current_level

    @property
    def player(self):
        return self._player

    @property
    def locks(self):
        return self._locks

    @property
    def beam_barriers(self):
        return self._beam_barriers

    @property
    def teleports(self):
        return self._teleports

    @property
    def container(self):
        return self._container

    @property
    def exit_point(self):
        return self._exit_point

    @property
    def sound_player(self):
        return self._sound_player

    @property
    def magnetic_fields(self):
        return self._magnetic_fields

    @property
    def info_areas(self):
        return self._info_areas

    @property
    def nothrust(self):
        return self._nothrust

    @property
    def rails(self):
        return self._rails

    @property
    def enemies(self):
        return self._enemies

    @property
    def items(self):
        return self._items

    @property
    def animations(self):
        return self._animations

    @property
    def particles_manager(self):
        return self._particles_manager

    @property
    def board(self):
        return self._board

    @property
    def powerups(self):
        return self._powerups

    @property
    def life_exchangers(self):
        return self._life_exchangers
