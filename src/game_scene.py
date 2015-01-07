import pygame
import board
import control
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
        self.items = None
        self.level01 = context.resourcemanager.get('level01')
        self.renderobj = None
        self.particlesmanager = particles_manager.ParticlesManager()
        beam_particles = particles.BeamParticles(context, 'hit')
        self.particlesmanager.register_particles(beam_particles)
        context.particlesmanager = self.particlesmanager
        self.player = player.Player(context, self.level01)
        self.board = board.Board(context, self.player)
        self.animations = context.resourcemanager.animations
        self.resourcemanager = context.resourcemanager
        self.laser = context.resourcemanager.get('laser')
        self.song = context.resourcemanager.get('level01_song')
        self.music = self.song
        self.get_menu()

    def on_start(self):
        self.player.on_start()
        self.menu_group.visible = False
        self.current_level = self.level01
        self.items = item.ItemBuilder.build(self.resourcemanager, self.current_level.items)
        self.renderobj = renderer.Renderer(self)
        self.music.play(-1)

    def on_quit(self):
        self.music.stop()

    def run(self):
        if self.menu_group.visible:
            self.menu_group.run()
        else:

            if not self.player.recovery_mode and self.player.life < 100:

                if self.player.recovery_counter < 100 :
                    self.player.recovery_counter += 1

                if self.player.recovery_counter == 100:
                    self.player.recovery_mode = True

            if self.control.on(control.Control.RIGHT):
                self.player.recovery_counter = 0
                self.player.recovery_mode = False
                #if not self.player.check_right_collision(self.current_level):
                self.player.direction = 1
                self.player.x += self.renderobj.speed[0]
            if self.control.on(control.Control.LEFT):
                self.player.recovery_counter = 0
                self.player.recovery_mode = False
                #if not self.player.check_left_collision(self.current_level):
                self.player.direction = -1
                self.player.x -= self.renderobj.speed[0]

            if self.control.on(control.Control.DOWN):
                self.player.life -= 1
                # Checks if player is over an item

                for i in self.items:
                    x = self.player.x
                    y = self.player.y
                    w = self.player.w
                    h = self.player.h

                    if x + 8 >= i.x and x - 8 <= i.x + i.w and y + 8 >= i.y and y - 8 <= i.y + i.h:
                        # Player is over an item

                        if not self.player.selected_item:
                            self.player.selected_item = i
                            self.items.remove(i)
                            self.renderobj.change_animation((i.x, i.y), None)
                        else:
                            tmp_item = self.player.selected_item
                            self.player.selected_item = i
                            x, y = i.x, i.y
                            self.items.remove(i)
                            tmp_item.x, tmp_item.y = x, y
                            self.items.append(tmp_item)
                            self.renderobj.change_animation((i.x, i.y), tmp_item.name)
            
            if self.control.on(control.Control.UP) and self.player.thrust > 0:
                self.player.recovery_counter = 0
                self.player.recovery_mode = False
                self.player.thrust -= .1
                if not self.player.check_upper_collision(self.current_level):
                    self.player.y -= self.renderobj.speed[1]
            else:
                if not self.player.check_bottom_collision(self.current_level):
                    self.player.y += self.renderobj.speed[1]

            if self.control.on(control.Control.ACTION1) and self.player.shoot_avail and self.player.bullets > 0:
                self.player.recovery_counter = 0
                self.player.recovery_mode = False
                self.laser.play()
                self.player.firing = True
                self.player.bullets -= .3

            if self.control.on(control.Control.ACTION2):
                self.player.using_item = True
                self.menu_group.visible = True

        self.player.run()
        self.particlesmanager.run()
        self.renderobj.run()

    def render(self, scr):
        self.renderobj.render()

        if self.menu_group.visible:
            self.menu_group.render(scr.virt, (128, 70))
