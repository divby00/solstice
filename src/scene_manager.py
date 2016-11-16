import pygame
import config


class SceneManager(object):
    def __init__(self, context, start_scene):
        self.screen = context.scr
        self.scenes = context.scenes
        self.cfg = context.cfg

        for scene in self.scenes:
            self.scenes[scene].scenemanager = self

            if scene == start_scene:
                self.scene = self.scenes[scene]
                self.current_scene = self.scene
                self.set(start_scene)

    def set(self, scene_name):
        self.name = scene_name
        self.current_scene.on_quit()
        self.scene = self.scenes[scene_name]
        self.current_scene = self.scene
        self.fps = self.scene.scene_speed
        self.clock = pygame.time.Clock()
        self.scene.running = True
        self.scene.on_start()

    def run(self):

        while self.scene.running:

            self.scene.keyboard_event = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.scene.running = False
                if event.type == pygame.KEYDOWN:
                    self.scene.keyboard_event = event
                if event.type == pygame.VIDEORESIZE:
                    self.screen.resize_window(event)
                    self._update_window_size_in_config(event.size)

            self.scene.run()
            self.scene.render(self.screen)
            pygame.transform.scale(self.screen.virt,
                                   self.screen.scaling_resolution,
                                   self.screen.scaled_virt)
            self.screen.display.blit(self.screen.scaled_virt, (self.screen.final_offset))

            pygame.display.update()
            self.clock.tick(self.fps)

    def _update_window_size_in_config(self, size):
        self.cfg.parser.set(config.Configuration.SECTION[1],
                            config.Configuration.OPT_SCREEN_WIDTH,
                            size[0])
        self.cfg.parser.set(config.Configuration.SECTION[1],
                            config.Configuration.OPT_SCREEN_HEIGHT,
                            size[1])

