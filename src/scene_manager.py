import pygame
import scene


class SceneManager(object):

    def __init__(self, context):
        self.screen = context.scr

    def set(self, scene):
        self.scene = scene
        self.fps = self.scene.scene_speed
        self.clock = pygame.time.Clock()
        self.scene.running = True

    def run(self):

        while self.scene.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.scene.running = False

            self.scene.run()
            self.scene.render(self.screen)
            pygame.transform.scale(self.screen.virt,
                                   self.screen.screen_size,
                                   self.screen.display)
            pygame.display.update()
            self.clock.tick(self.fps)
