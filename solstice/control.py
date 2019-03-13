# -*- coding: utf-8 -*-

from gettext import gettext as _

import pygame
from enum import IntEnum, Enum


class ControlActionType(IntEnum):
    KEY_PRESS = 0,
    BUTTON_PRESS = 1,
    AXIS_CHANGED = 2


class ControlMovement(Enum):
    UP = 'up',
    DOWN = 'down',
    LEFT = 'left',
    RIGHT = 'right',
    ACTION1 = 'action1',
    ACTION2 = 'action2',
    START = 'start'


class ControlAction(object):

    def __init__(self, name, mapping, control_type=ControlActionType.KEY_PRESS, axis=None):
        self._name = name
        self._mapping = mapping
        self._type = control_type
        self._axis = axis

    @property
    def name(self):
        return self._name

    @property
    def mapping(self):
        return self._mapping

    @property
    def type(self):
        return self._type

    @property
    def axis(self):
        return self._axis


class ControlInput(object):

    def __init__(self, actions):
        self._actions = actions

    def update(self):
        raise NotImplementedError('Not yet implemented')

    def on(self, control_action):
        raise NotImplementedError('Not yet implemented')


class KeyboardInput(ControlInput):

    def __init__(self, actions):
        super(KeyboardInput, self).__init__(actions)
        self._keys = None

    def update(self):
        self._keys = pygame.key.get_pressed()

    def on(self, action_name, keyboard_event=None):
        for action in self._actions:
            if action.name == action_name:
                if keyboard_event:
                    if keyboard_event.key == action.mapping:
                        return True
                else:
                    if self._keys[action.mapping]:
                        return True
        return False


class JoystickInput(ControlInput):

    def __init__(self, actions, joystick):
        super(JoystickInput, self).__init__(actions)
        self._joystick = joystick
        self._joystick.init()
        self._buttons = range(self._joystick.get_numbuttons())
        self._axes = range(self._joystick.get_numaxes())

    def update(self):
        pass

    def on(self, action_name, joystick_event=None):
        for action in self._actions:
            if action.name == action_name:
                if joystick_event:
                    if joystick_event.key == action.mapping:
                        return True
                else:
                    if action.type == ControlActionType.BUTTON_PRESS and action.mapping in self._buttons:
                        return self._joystick.get_button(action.mapping)

                    if action.type == ControlActionType.AXIS_CHANGED and action.axis in self._axes:
                        return self._joystick.get_axis(action.axis) > 0 and action.mapping > 0 \
                               or self._joystick.get_axis(action.axis) < 0 and action.mapping < 0

        return False


class UndefinedDeviceError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Control(object):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    ACTION1 = 'action1'
    ACTION2 = 'action2'
    START = 'start'

    def __init__(self, context):
        pygame.key.set_repeat()
        self._config = context.config
        self._keyboard_event = None
        self._joystick_event = None
        self._event_driven = True
        self._devices = self._register_devices()

    def _register_devices(self):
        devices = []
        actions = []

        if self._config.control_type in ['autodetect', 'keyboard']:
            actions.append(ControlAction(Control.UP, self._config.key_up))
            actions.append(ControlAction(Control.DOWN, self._config.key_down))
            actions.append(ControlAction(Control.LEFT, self._config.key_left))
            actions.append(ControlAction(Control.RIGHT, self._config.key_right))
            actions.append(ControlAction(Control.ACTION1, self._config.key_act1))
            actions.append(ControlAction(Control.ACTION2, self._config.key_act2))
            actions.append(ControlAction(Control.START, self._config.key_start))
            devices.append(KeyboardInput(actions))

        if self._config.control_type in ['autodetect', 'joystick']:
            if pygame.joystick.get_count() > 0:
                joystick_device = pygame.joystick.Joystick(0)
                actions.append(ControlAction(Control.UP, self._config.axis_up, ControlActionType.AXIS_CHANGED,
                                             self._config.vertical_axis))
                actions.append(ControlAction(Control.DOWN, self._config.axis_down, ControlActionType.AXIS_CHANGED,
                                             self._config.vertical_axis))
                actions.append(ControlAction(Control.LEFT, self._config.axis_left, ControlActionType.AXIS_CHANGED,
                                             self._config.horizontal_axis))
                actions.append(ControlAction(Control.RIGHT, self._config.axis_right, ControlActionType.AXIS_CHANGED,
                                             self._config.horizontal_axis))
                actions.append(ControlAction(Control.ACTION1, self._config.button_act1, ControlActionType.BUTTON_PRESS))
                actions.append(ControlAction(Control.ACTION2, self._config.button_act2, ControlActionType.BUTTON_PRESS))
                devices.append(JoystickInput(actions, joystick_device))

        if len(devices) == 0:
            raise UndefinedDeviceError(_('Unable to set a control device.'))

        return devices

    def on(self, action_name):
        if self._event_driven:
            if self._keyboard_event:
                for device in self._devices:
                    if device.on(action_name, self._keyboard_event):
                        return True
            if self._joystick_event:
                for device in self._devices:
                    if device.on(action_name, self._joystick_event):
                        return True
        else:
            pygame.event.pump()
            for device in self._devices:
                device.update()
                if device.on(action_name):
                    return True

        return False

    @property
    def keyboard_event(self):
        return self._keyboard_event

    @keyboard_event.setter
    def keyboard_event(self, value):
        self._keyboard_event = value

    @property
    def joystick_event(self):
        return self._joystick_event

    @joystick_event.setter
    def joystick_event(self, value):
        self._joystick_event = value

    @property
    def event_driven(self):
        return self._event_driven

    @event_driven.setter
    def event_driven(self, value):
        self._event_driven = value
