import board
import scene
import control


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
        self.select_floor = self.font_white.get('Elevator - select floor', 240)
        self.cursor = context.resourcemanager.get('cursor')
        self._cursor_position = 0
        self.unblocked_floors = {}
        self.blocked_floors = {}
        for key in floors.iterkeys():
            self.unblocked_floors.update({key: self.font_yellow.get(key + ': access granted', 160)})
            self.blocked_floors.update({key: self.font_blue.get(key + ': access blocked', 160)})

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
        self._cursor_position = 0
        self.control.event_driven = True

    def on_quit(self):
        pass

    def render(self, scr):
        scr.virt.fill((0, 0, 0))
        scr.virt.blit(self.select_floor, (16, 16))
        i = 32

        for key in sorted(floors.keys()):
            spr = self.blocked_floors[key] if not floors[key] else self.unblocked_floors[key]
            scr.virt.blit(spr, (32, i))
            i = i + 10

        scr.virt.blit(self.cursor, (16, (self._cursor_position * 10) + 32))

        # Board rendering
        self._board.render(self._screen.virt)

    def run(self):
        self.control.event_driven = True
        self.control.keyboard_event = self.keyboard_event

        if self.control.on(control.Control.ACTION1):
            self.sound_player.play_sample('accept')
            self.scenemanager.set('game', self._cursor_position + 1)

        if self.control.on(control.Control.UP):
            self._cursor_position = self._cursor_position - 1
            if self._cursor_position == -1:
                self._cursor_position = 7
            self.sound_player.play_sample('blip')

        if self.control.on(control.Control.DOWN):
            self._cursor_position = self._cursor_position + 1
            if self._cursor_position == 8:
                self._cursor_position = 0
            self.sound_player.play_sample('blip')
