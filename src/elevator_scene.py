import board
import scene


floors = {
    '01': True, '02': False,
    '03': False, '04': False,
    '05': False, '06': False,
    '07': False, '08': False
}


class ElevatorScene(scene.Scene):

    def __init__(self, context, name='elevator', scene_speed=25):
        super(ElevatorScene, self).__init__(context, name, scene_speed)
        self._context = context
        self._screen = context.scr
        self._board = None
        self.select_floor = self.font_white.get('Select floor', 200)
        self.unblocked_floors = {}
        self.blocked_floors = {}
        for key in floors.iterkeys():
            self.unblocked_floors.update({key: self.font_yellow.get(key, 3)})
            self.blocked_floors.update({key: self.font_blue.get(key, 3)})

    def _open_floor(self, card):
        for key in floors.iterkeys():
            if key == card.card_id:
                floors[key] = True

    def on_start(self):
        # Note that at this point, self.scene_data has been 'injected' from scene_manager
        # Scene data contains the player info, it's needed to properly render the board
        self.scene_data.continuos_hit = 0
        self._open_floor(self.scene_data.selected_item)
        self.scene_data.selected_item = None
        self._board = board.Board(self._context, self.scene_data)

    def render(self, scr):
        scr.virt.fill((0, 0, 0))
        scr.virt.blit(self.select_floor, (16, 16))
        i = 32

        for key in sorted(floors.keys()):
            spr = self.blocked_floors[key] if not floors[key] else self.unblocked_floors[key]
            scr.virt.blit(spr, (80, i))
            i = i + 10

        # Board rendering
        self._board.render(self._screen.virt)

    def run(self):
        pass
