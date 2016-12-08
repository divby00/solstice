import pygame
import board
import scene
import control


floors = {
    '01': True, '02': False,
    '03': False, '04': False,
    '05': False, '06': False,
    '07': False, '08': False
}


class UIManager(object):

    def __init__(self, context, sound_player):
        self._resource_manager = context.resourcemanager
        self._sound_player = sound_player
        self._buttons = self._init_buttons()
        self._tabindex = 0
        self._max_tabindex = len(self._buttons) - 1
        self._set_focus()

    def _init_buttons(self):
        button_positions = [
            (32, 28), (56, 28), (32, 48), (56, 48),
            (32, 68), (56, 68), (32, 88), (56, 88),
            (32, 108)
        ]
        button_labels = [
            '01', '02', '03', '04',
            '05', '06', '07', '08',
            'go'
        ]
        button_sizes = [
            (16, 16), (16, 16), (16, 16), (16, 16),
            (16, 16), (16, 16), (16, 16), (16, 16),
            (40, 16)
        ]
        buttons = []
        for index, val in enumerate(button_labels):
            disabled_spr = self._resource_manager.get('disabled_btn' + val)
            pressed_spr = self._resource_manager.get('pressed_btn' + val)
            buttons.append(ElevatorButton(index, (pressed_spr, disabled_spr), button_positions[index], button_sizes[index]))
        return buttons

    def _render_buttons(self, scr):
        for btn in self._buttons:
            sprite = None
            if btn.disabled:
                sprite = btn.sprites['disabled']
            if btn.pressed:
                sprite = btn.sprites['pressed']
            if sprite is not None:
                scr.virt.blit(sprite, btn.position)

    def _render_focus(self, scr):
        position = self._buttons[self._tabindex].position
        size = self._buttons[self._tabindex].size
        pygame.draw.rect(scr.virt, (49, 162, 242),
                         (position[0] - 1, position[1] - 1, size[0] + 2, size[1] + 2), 1)

    def _set_focus(self):
        for btn in self._buttons:
            btn.focus = False
        self._buttons[self._tabindex].focus = True

    def render(self, scr):
        self._render_buttons(scr)
        self._render_focus(scr)

    def run(self, ctrl):
        if ctrl.on(control.Control.UP) or ctrl.on(control.Control.LEFT):
            self._tabindex = self._tabindex - 1
            self._sound_player.play_sample('blip')
            if self._tabindex == -1:
                self._tabindex = self._max_tabindex

        if ctrl.on(control.Control.DOWN) or ctrl.on(control.Control.RIGHT):
            self._tabindex = self._tabindex + 1
            self._sound_player.play_sample('blip')
            if self._tabindex == self._max_tabindex + 1:
                self._tabindex = 0

        if ctrl.on(control.Control.ACTION1):
            for btn in self._buttons:
                if not btn.disabled:
                    btn.pressed = False
            if not self._buttons[self._tabindex].pressed:
                self._buttons[self._tabindex].pressed = True
                self._sound_player.play_sample('accept')

        self._set_focus()

class ElevatorButton(object):

    def __init__(self, index, sprites, position, size):
        self._disabled = False
        self._pressed = False
        self._focus = False
        self._position = position
        self._size = size
        self._tabindex = index
        self._sprites = {
            'pressed': sprites[0],
            'disabled': sprites[1]
        }

    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, value):
        self._focus = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def sprites(self):
        return self._sprites

    @property
    def disabled(self):
        return self._disabled

    @property
    def pressed(self):
        return self._pressed

    @pressed.setter
    def pressed(self, value):
        self._pressed = value

    @property
    def position(self):
        return self._position


class DummyPlayer(object):

    def __init__(self):
        self.continuos_hit = 0
        self.lives = 3
        self.life = 100
        self.thrust = 100
        self.bullets = 50


class ElevatorScene(scene.Scene):

    def __init__(self, context, name='elevator', scene_speed=25):
        super(ElevatorScene, self).__init__(context, name, scene_speed)
        self._context = context
        self._screen = context.scr
        self._ui_manager = UIManager(context, self.sound_player)
        self._board = None
        self.select_floor = self.font_white.get('Elevator - select floor', 240)
        self._selected_levels = self._get_selected_levels_spr()
        self._panel = context.resourcemanager.get('elev_panel')

    def _get_selected_levels_spr(self):
        return [self._context.resourcemanager.get('selected_lvl0' + str(btn)) for btn in xrange(1, 9)]

    def _open_floor(self, card_id):
        for key in floors.iterkeys():
            if key == card_id:
                floors[key] = True

    def dummy_scene_data(self):
        self.scene_data = DummyPlayer()

    def on_start(self):
        self.dummy_scene_data()
        # Note that at this point, self.scene_data has been 'injected' from scene_manager
        # Scene data contains the player info, it's needed to properly render the board
        self.scene_data.continuos_hit = 0
        self._open_floor('02')
        #self._open_floor(self.scene_data.selected_item.card_id)
        self.scene_data.selected_item = None
        self._board = board.Board(self._context, self.scene_data)
        self._cursor_position = 0
        self.control.event_driven = True

    def on_quit(self):
        pass

    def render(self, scr):
        # scr.virt.fill((47, 72, 78))
        scr.virt.fill((0, 0, 0))
        scr.virt.blit(self.select_floor, (36, 4))
        scr.virt.blit(self._panel, (16, 16))
        self._ui_manager.render(scr)
        # Board rendering
        self._board.render(self._screen.virt)

    def run(self):
        self.control.event_driven = True
        self.control.keyboard_event = self.keyboard_event
        self._ui_manager.run(self.control)
