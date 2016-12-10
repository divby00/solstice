import pygame

import board
import control
import scene

floors = {
    '01': True, '02': False,
    '03': False, '04': False,
    '05': False, '06': False,
    '07': False, '08': False
}


class ElevatorUiManager(object):
    def __init__(self, context, sound_player):
        self._resource_manager = context.resourcemanager
        self._blue_font = self._resource_manager.get('font_blue')
        self._red_font = self._resource_manager.get('font_red')
        self._small_blue_font = self._resource_manager.get('font_small_blue')
        self._small_red_font = self._resource_manager.get('font_small_red')
        self._sound_player = sound_player
        self._panel = self._init_panel()
        self._buttons = self._init_buttons()
        self._floors = self._init_floors()
        self._info = self._init_info()
        self._txt_access_denied = self._red_font.get('Access denied', 1)
        self._txt_access_allowed = self._blue_font.get('Access allowed', 1)
        self._selected_floor = self._floors[0]
        self._tabindex = 0
        self._max_tabindex = len(self._buttons) - 1
        self._set_focus()

    def _init_info(self):
        level_info = [
            {
                'enemies': 'Alpha Medusoid, Green Devil',
                'frequency': 'low',
                'teleporters': '2',
                'tips': "First approach. Enemy concentration is lower than it's in areas below"
            },
            {
                'enemies': 'Alpha Medusoid, Splitter, High Devil',
                'frequency': 'low',
                'teleporters': '4'
            },
            {
                'enemies': 'Gamma Medusoid, Alpha Medusoid, Splitter',
                'frequency': 'normal',
                'teleporters': '4'
            }
        ]
        return level_info

    def _init_panel(self):
        return ElevatorPanel(self._resource_manager, (16, 16))

    def _init_floors(self):
        floor_positions = [
            (111, 27), (111, 41), (111, 52), (111, 67),
            (111, 77), (111, 87), (111, 105), (111, 115),
        ]
        return [ElevatorFloor(self._resource_manager, i, floor_positions[i - 1]) for i in xrange(1, 9)]

    def _init_buttons(self):
        button_positions = [
            (32, 32), (56, 32), (32, 56), (56, 56),
            (32, 80), (56, 80), (32, 104), (56, 104)
        ]
        button_labels = [
            '01', '02', '03', '04',
            '05', '06', '07', '08'
        ]
        button_sizes = [
            (16, 16), (16, 16), (16, 16), (16, 16),
            (16, 16), (16, 16), (16, 16), (16, 16)
        ]
        buttons = []
        for index, val in enumerate(button_labels):
            disabled_spr = self._resource_manager.get('disabled_btn' + val)
            pressed_spr = self._resource_manager.get('pressed_btn' + val)
            buttons.append(ElevatorButton(index, (pressed_spr, disabled_spr),
                                          button_positions[index], button_sizes[index]))

        for index, btn in enumerate(buttons):
            btn.disabled = False if floors[button_labels[index]] else True

        return buttons

    def _render_info(self, scr):
        txt = self._txt_access_allowed if not self._buttons[self._tabindex].disabled else self._txt_access_denied
        scr.virt.blit(txt, (148, 24))

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

        # Render the selected level
        floor_sprite = self._selected_floor.sprite if not self._buttons[self._tabindex].disabled \
            else self._selected_floor.blocked_sprite
        scr.virt.blit(floor_sprite, self._selected_floor.position)

    def _render_panel(self, scr):
        scr.virt.blit(self._panel.sprite, self._panel.position)

    def _set_focus(self):
        for btn in self._buttons:
            btn.focus = False
        self._buttons[self._tabindex].focus = True

    def render(self, scr):
        self._render_panel(scr)
        self._render_info(scr)
        self._render_buttons(scr)
        self._render_focus(scr)

    def run(self, ctrl):
        if ctrl.on(control.Control.UP) or ctrl.on(control.Control.LEFT):
            self._tabindex -= 1
            self._sound_player.play_sample('blip')
            self._selected_floor = self._floors[self._tabindex]
            if self._tabindex == -1:
                self._tabindex = self._max_tabindex
                self._selected_floor = self._floors[self._tabindex]
            self._set_focus()

        if ctrl.on(control.Control.DOWN) or ctrl.on(control.Control.RIGHT):
            self._tabindex += 1
            self._sound_player.play_sample('blip')
            if self._tabindex == self._max_tabindex + 1:
                self._tabindex = 0
            self._selected_floor = self._floors[self._tabindex]
            self._set_focus()

        if ctrl.on(control.Control.ACTION1):
            if self._buttons[self._tabindex].disabled:
                self._sound_player.play_sample('cancel')
                return

            if not self._buttons[self._tabindex].pressed:
                for btn in self._buttons:
                    if not btn.disabled:
                        btn.pressed = False
                self._buttons[self._tabindex].pressed = True
                self._sound_player.play_sample('accept')


class ElevatorPanel(object):
    def __init__(self, resource_manager, position):
        self._sprite = resource_manager.get('elev_panel')
        self._position = position

    @property
    def sprite(self):
        return self._sprite

    @property
    def position(self):
        return self._position


class ElevatorFloor(object):
    def __init__(self, resource_manager, floor, position):
        self._selected = False
        self._sprite = resource_manager.get('selected_lvl0' + str(floor))
        self._blocked_sprite = resource_manager.get('blocked_lvl0' + str(floor))
        self._floor = floor
        self._position = position

    @property
    def sprite(self):
        return self._sprite

    @property
    def blocked_sprite(self):
        return self._blocked_sprite

    @property
    def selected(self):
        return self._selected

    @property
    def position(self):
        return self._position


class ElevatorButton(object):
    def __init__(self, index, sprites, position, size):
        self._pressed = False
        self._focus = False
        self._position = position
        self._disabled = False
        self._size = size
        self._tabindex = index
        self._sprites = {
            'pressed': sprites[0],
            'disabled': sprites[1]
        }

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        self._disabled = value

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
    @staticmethod
    def open_floor(card_id):
        for key in floors.iterkeys():
            if key == card_id:
                floors[key] = True

    def __init__(self, context, name='elevator', scene_speed=25):
        super(ElevatorScene, self).__init__(context, name, scene_speed)
        self._context = context
        self._screen = context.scr
        self._ui_manager = None
        self._board = None
        self._txt_select_floor = self.font_white.get('Elevator - select floor', 240)

    def dummy_scene_data(self):
        self.scene_data = DummyPlayer()

    def on_start(self):
        self.dummy_scene_data()
        # Note that at this point, self.scene_data has been 'injected' from scene_manager
        # Scene data contains the player info, it's needed to properly render the board
        self.scene_data.continuos_hit = 0
        ElevatorScene.open_floor('02')
        # ElevatorScene.open_floor(self.scene_data.selected_item.card_id)
        self._ui_manager = ElevatorUiManager(self._context, self.sound_player)
        self.scene_data.selected_item = None
        self._board = board.Board(self._context, self.scene_data)
        self.control.event_driven = True

    def on_quit(self):
        pass

    def render(self, scr):
        # scr.virt.fill((47, 72, 78))
        scr.virt.fill((0, 0, 0))
        scr.virt.blit(self._txt_select_floor, (36, 4))
        self._ui_manager.render(scr)
        self._board.render(self._screen.virt)

    def run(self):
        self.control.event_driven = True
        self.control.keyboard_event = self.keyboard_event
        self._ui_manager.run(self.control)
