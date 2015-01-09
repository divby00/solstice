import pygame
import board
import control
import lock
import item
import player
import scene
import particles_manager
import particles
import renderer


class GameScene(scene.Scene):

    def __init__(self, context, name='game', scene_speed=25):
        super(GameScene, self).__init__(context, name, scene_speed)
        self.screen = context.scr
        self.locks = None
        self.items = None
        self.level01 = context.resourcemanager.get('level01')
        self.renderobj = None
        self.particlesmanager = particles_manager.ParticlesManager()
        beam_particles = particles.BeamParticles(context, 'hit')
        exp_particles = particles.ExplosionParticles(context, 'exp')
        self.particlesmanager.register_particles(beam_particles)
        self.particlesmanager.register_particles(exp_particles)
        context.particlesmanager = self.particlesmanager
        self.player = player.Player(context, self.level01)
        self.board = board.Board(context, self.player)
        self.animations = context.resourcemanager.animations
        self.resourcemanager = context.resourcemanager
        self.laser = context.resourcemanager.get('laser')
        self.use_item = context.resourcemanager.get('accept')
        self.no_item = context.resourcemanager.get('cancel')
        self.bulletsup = context.resourcemanager.get('bulletsup')
        self.thrustup = context.resourcemanager.get('thrustup')
        self.song = context.resourcemanager.get('level01_song')
        self.exp = context.resourcemanager.get('exp')
        self.music = self.song
        self.get_menu()

    def on_start(self):
        self.player.on_start()
        self.menu_group.visible = False
        self.current_level = self.level01
        self.locks = lock.LockBuilder.build(self, self.resourcemanager, self.current_level.locks)
        self.items = item.ItemBuilder.build(self, self.resourcemanager, self.current_level.items)
        self.renderobj = renderer.Renderer(self)
        self.music.play(-1)

    def get_renderer(self):
        return self.renderobj

    def get_layers(self):
        return self.current_level.layers

    def on_quit(self):
        self.music.stop()

    def run(self):
        if self.menu_group.visible:
            self.menu_group.run()
        else:

            if self.player.get_item_counter < 5:
                self.player.get_item_counter += 1
                
                if self.player.get_item_counter == 5:
                    self.player.get_item_available = True

            if not self.player.recovery_mode and self.player.life < 100:

                if self.player.recovery_counter < 100 :
                    self.player.recovery_counter += 1

                if self.player.recovery_counter == 100:
                    self.player.recovery_mode = True

            if self.control.on(control.Control.RIGHT):
                self.player.recovery_counter = 0
                self.player.recovery_mode = False

                # if not self.player.check_right_collision(self.current_level):
                self.player.direction = 1
                self.player.x += self.renderobj.speed[0]

            if self.control.on(control.Control.LEFT):
                self.player.recovery_counter = 0
                self.player.recovery_mode = False

                # if not self.player.check_left_collision(self.current_level):
                self.player.direction = -1
                self.player.x -= self.renderobj.speed[0]

            if self.control.on(control.Control.UP) and self.player.thrust > 0:
                self.player.recovery_counter = 0
                self.player.recovery_mode = False
                self.player.thrust -= .1
                if not self.player.check_upper_collision(self.current_level):
                    self.player.y -= self.renderobj.speed[1]
            else:
                if not self.player.check_bottom_collision(self.current_level):
                    self.player.y += self.renderobj.speed[1]

            if self.control.on(control.Control.DOWN):
                self.player.recovery_mode = False
                self.player.recovery_counter = 0

                # Checks if player is over an item
                if self.player.get_item_available:
                    item_found = False
                    x = self.player.x
                    y = self.player.y
                    w = self.player.w
                    h = self.player.h

                    for i in self.items:

                        if x + 8 >= i.x and x - 8 <= i.x + i.w and y + 8 >= i.y and y - 8 <= i.y + i.h:
                            # Player is over an item
                            item_found = True
                            self.player.get_item_available = False
                            self.player.get_item_counter = 0
                            self.use_item.play()

                            if not self.player.selected_item:
                                self.player.selected_item = i
                                self.items.remove(i)
                                self.renderobj.change_animation((i.x, i.y), None)
                            else:
                                tmp_item = self.player.selected_item
                                x, y = i.x, i.y
                                self.player.selected_item = i
                                self.items.remove(i)
                                tmp_item.x, tmp_item.y = x, y
                                self.items.append(tmp_item)
                                self.renderobj.change_animation((i.x, i.y), tmp_item.name)
                                break
            
            if self.control.on(control.Control.ACTION1) and self.player.shoot_avail and self.player.bullets > 0:
                self.player.recovery_counter = 0
                self.player.recovery_mode = False
                self.laser.play()
                self.player.firing = True
                self.player.bullets -= .3

            if self.control.on(control.Control.ACTION2):
                self.player.recovery_counter = 0
                self.player.recovery_mode = False

                if self.player.selected_item is not None:
                    self.player.life -= 1
                    self.player.using_item = True
                    self.use_item.play()

            if self.control.on(control.Control.START):
                self.menu_group.visible = True

        self.player.run()
        self.particlesmanager.run()
        self.renderobj.run()

    def render(self, scr):
        self.renderobj.render()

        if self.menu_group.visible:
            self.menu_group.render(scr.virt, (128, 70))
