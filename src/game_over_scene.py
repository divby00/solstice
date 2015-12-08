import scene


class GameOverScene(scene.Scene):

    def __init__(self, context, name='game_over', scene_speed=25):
        super(GameOverScene, self).__init__(context, name, scene_speed)

    def on_start(self):
        raise NotImplementedError('Implement this method')

    def render(self, scr):
        raise NotImplementedError('Implement this method')

    def run(self):
        raise NotImplementedError('Implement this method')
