import pygame
import config
import transition_manager


class SceneManager(object):
    def __init__(self, context, start_scene):
        self._temp_scene = None
        self._temp_scene_data = None
        self.screen = context.scr
        self.scenes = context.scenes
        self.cfg = context.cfg
        self._transition_manager = transition_manager.TransitionManager(context.resourcemanager)

        for scene in self.scenes:
            self.scenes[scene].scenemanager = self

            if scene == start_scene:
                self.scene = self.scenes[scene]
                self.current_scene = self.scene
                self.set(start_scene)

    @property
    def transition_manager(self):
        return self._transition_manager

    def set(self, scene_name, scene_data=None):
        self.name = scene_name
        self.current_scene.on_quit()
        self.scene = self.scenes[self.name]
        self.current_scene = self.scene
        self.fps = self.scene.scene_speed
        # Horrible injection of custom data to scenes after their constructors have been called.
        # I will burn in hell for this.
        self.scenes[self.name].scene_data = scene_data
        self.clock = pygame.time.Clock()
        self.scene.running = True
        self.scene.on_start()

        if scene_name == 'logo':
            self._transition_manager.set('dummy')
        else:
            self._transition_manager.set('squares_in')
        self._transition_manager.start()

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
            self._transition_manager.run()
            self.scene.render(self.screen)
            self._transition_manager.render(self.screen)
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

