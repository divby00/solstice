import board
import scene


class ElevatorScene(scene.Scene):

    def __init__(self, context, name='elevator', scene_speed=25):
        super(ElevatorScene, self).__init__(context, name, scene_speed)
        self._context = context
        self._screen = context.scr
        self._board = None
        self.scene_data = None

    def _create_fake_player(self):
        pass

    def on_start(self):
        # Note that at this point, self.scene_data has been 'injected' from scene_manager
        self._board = board.Board(self._context, self.scene_data)

    def render(self, scr):
        scr.virt.fill((0, 0, 0))
        # Board rendering
        self._board.render(self._screen.virt)

    def run(self):
        pass



