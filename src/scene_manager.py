import pygame


class SceneManager(object):
    def __init__(self, context, start_scene):
        self.screen = context.scr
        self.scenes = context.scenes

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
