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
    def __init__(self, context, player_floor, sound_player):
        self._resource_manager = context.resourcemanager
        self._scene_manager = context.scenemanager
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
        self._player_floor = player_floor
        self._player_mark = self._init_player_mark()
        self._selected_floor = self._floors[self._player_floor]
        self._tabindex = self._player_floor
        self._max_tabindex = len(self._buttons) - 1
        self._set_focus()

    '''
    Private methods
    '''

    def _init_info(self):
        level_info = [
            {
                'enemies': 'Alpha Medusoid, Green Devil',
                'frequency': 'low',
                'teleporters': '2',
                'tips': "First approach. Enemy concentration is higher in areas below"
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

    def _init_player_mark(self):
        return ElevatorPlayerMark(self._resource_manager, self._player_floor)

    def _init_panel(self):
        return ElevatorPanel(self._resource_manager, (16, 16))

    def _init_floors(self):
        floor_positions = [
            (111, 27), (111, 41), (111, 52), (111, 67),
            (111, 77), (111, 87), (111, 105), (111, 115),
        ]
        return [ElevatorFloor(self._resource_manager, i, floor_positions[i - 1]) for i in
                xrange(1, 9)]

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
            buttons.append(ElevatorButton(index,
                                          (pressed_spr, disabled_spr),
                                          button_positions[index], button_sizes[index]))

        for index, btn in enumerate(buttons):
            btn.disabled = False if floors[button_labels[index]] else True

        return buttons

    def _render_info(self, scr):
        txt = self._txt_access_allowed if not self._buttons[
            self._tabindex].disabled else self._txt_access_denied
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

    def _render_player_mark(self, scr):
        self._player_mark.render(scr)

    def _set_focus(self):
        for btn in self._buttons:
            btn.focus = False
        self._buttons[self._tabindex].focus = True

    '''
    Public methods
    '''

    def render(self, scr):
        self._render_panel(scr)
        self._render_info(scr)
        self._render_buttons(scr)
        self._render_focus(scr)
        self._render_player_mark(scr)

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
                self._scene_manager.set('game', self._tabindex)

        self._player_mark.run()


class ElevatorPanel(object):
    def __init__(self, resource_manager, position):
        self._sprite = resource_manager.get('elev_panel')
        self._position = position

    '''
    Public methods
    '''

    @property
    def sprite(self):
        return self._sprite

    @property
    def position(self):
        return self._position


class ElevatorPlayerMark(object):
    def __init__(self, resource_manager, player_floor):
        positions = [
            (116, 33), (116, 40), (116, 33), (116, 40),
            (116, 33), (116, 40), (116, 33), (116, 40)
        ]
        self._sprites = [resource_manager.get('mark' + str(index)) for index in xrange(0, 5)]
        self._position = positions[player_floor]
        self._frame = 0

    '''
    Public methods
    '''

    @property
    def position(self):
        return self._position

    def render(self, scr):
        if self._frame < 5:
            scr.virt.blit(self._sprites[self._frame], self._position)

    def run(self):
        self._frame += 1
        if self._frame == 7:
            self._frame = 0


class ElevatorFloor(object):
    def __init__(self, resource_manager, floor, position):
        self._selected = False
        self._sprite = resource_manager.get('selected_lvl0' + str(floor))
        self._blocked_sprite = resource_manager.get('blocked_lvl0' + str(floor))
        self._floor = floor
        self._position = position

    '''
    Public methods
    '''

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

    '''
    Public methods
    '''

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
        self.floor = 2


class ElevatorScene(scene.Scene):
    def __init__(self, context, name='elevator', scene_speed=25):
        super(ElevatorScene, self).__init__(context, name, scene_speed)
        self._context = context
        self._screen = context.scr
        self._ui_manager = None
        self._board = None
        self._player_floor = 0
        self._txt_select_floor = self.font_white.get('Elevator - select floor', 240)

    '''
    Public methods
    '''

    @staticmethod
    def open_floor(card_id):
        for key in floors.iterkeys():
            if key == card_id:
                floors[key] = True

    def dummy_scene_data(self):
        self.scene_data = DummyPlayer()

    def on_start(self):
        # self.dummy_scene_data()
        # Note that at this point, self.scene_data has been 'injected' from scene_manager
        # Scene data contains the player info, it's needed to properly render the board
        self.scene_data.continuos_hit = 0
        self._player_floor = self.scene_data.floor
        if self.scene_data and self.scene_data.selected_item and 'card' in self.scene_data.selected_item.name:
            ElevatorScene.open_floor(self.scene_data.selected_item.card_id)
            self.scene_data.selected_item = None
        self._ui_manager = ElevatorUiManager(self._context, self._player_floor, self.sound_player)
        self._board = board.Board(self._context, self.scene_data)
        self.control.event_driven = True

    def on_quit(self):
        pass

    def render(self, scr):
        scr.virt.fill((47, 72, 78))
        # scr.virt.fill((0, 0, 0))
        scr.virt.blit(self._txt_select_floor, (36, 4))
        self._ui_manager.render(scr)
        self._board.render(self._screen.virt)

    def run(self):
        self.control.event_driven = True
        self.control.keyboard_event = self.keyboard_event

        # Fill player energy, laser & thrust
        if self.scene_data.life < 100:
            self.scene_data.life += 1
        if self.scene_data.thrust < 106:
            self.scene_data.thrust += 1
        if self.scene_data.bullets < 106:
            self.scene_data.bullets += 1
        self._ui_manager.run(self.control)
