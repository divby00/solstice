import pygame

import config
import transition_manager


class SceneManager(object):
    def __init__(self, context, start_scene):
        self._name = None
        self._fps = 0
        self._clock = None
        self._temp_scene = None
        self._temp_scene_data = None
        self._screen = context.screen
        self._scenes = context.scenes
        self._config = context.config
        self._current_scene = None
        self._transition_manager = transition_manager.TransitionManager(context.resource_manager)

        for scene in self._scenes:
            self._scenes[scene].scene_manager = self

            if scene == start_scene:
                self._scene = self._scenes[scene]
                self._current_scene = self._scene
                self.set(start_scene)

    '''
    Private methods
    '''

    def _update_window_size_in_config(self, size):
        self._config.parser.set(config.Configuration.SECTION[1],
                                config.Configuration.OPT_SCREEN_WIDTH, size[0])
        self._config.parser.set(config.Configuration.SECTION[1],
                                config.Configuration.OPT_SCREEN_HEIGHT, size[1])

    '''
    Public methods
    '''

    def set(self, scene_name, scene_data=None):
        self._name = scene_name
        self._current_scene.on_quit()
        self._scene = self._scenes[self._name]
        self._current_scene = self._scene
        self._fps = self._scene.scene_speed
        # Horrible injection of custom data to scenes after their constructors have been called.
        # I will burn in hell for this.
        self._scenes[self._name].scene_data = scene_data
        self._clock = pygame.time.Clock()
        self._scene.running = True
        self._scene.on_start()

        if scene_name == 'logo':
            self._transition_manager.set('dummy')
        elif scene_name == 'intro':
            self._transition_manager.set('circles_in')
        else:
            self._transition_manager.set('squares_in')
        self._transition_manager.start()

    def run(self):
        while self._scene.running:
            self._scene.keyboard_event = None
            self._scene.joystick_event = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._scene.running = False
                if event.type == pygame.KEYDOWN:
                    self._scene.keyboard_event = event
                if event.type == pygame.JOYBUTTONDOWN:
                    self._scene.joystick_event = event
                if event.type == pygame.VIDEORESIZE:
                    self._screen.resize_window(event)
                    self._update_window_size_in_config(event.size)

            self._scene.run()
            self._transition_manager.run()
            self._scene.render(self._screen)
            self._transition_manager.render(self._screen)
            pygame.transform.scale(self._screen.virt,
                                   self._screen.scaling_resolution,
                                   self._screen.scaled_virt)
            self._screen.display.blit(self._screen.scaled_virt, self._screen.final_offset)
            pygame.display.update()
            self._clock.tick(self._fps)

    @property
    def transition_manager(self):
        return self._transition_manager
