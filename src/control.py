import pygame
from gettext import gettext as _


class ControlAction(object):
    def __init__(self, name, mapping):
        self._name = name
        self._mapping = mapping

    '''
    Public methods
    '''

    @property
    def name(self):
        return self._name

    @property
    def mapping(self):
        return self._mapping


class ControlInput(object):
    def __init__(self, actions):
        self._actions = actions

    '''
    Public methods
    '''

    def update(self):
        raise NotImplementedError('Not yet implemented')

    def on(self, control_action):
        raise NotImplementedError('Not yet implemented')


class KeyboardInput(ControlInput):
    def __init__(self, actions):
        super(KeyboardInput, self).__init__(actions)
        self._keys = None

    '''
    Public methods
    '''

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

    '''
    Public methods
    '''

    def update(self):
        pass

    def on(self, action_name):
        pass


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
        self._event_driven = True
        joysticks = []
        self._devices = self._register_devices(joysticks)

    '''
    Private methods
    '''

    def _register_devices(self, joysticks):
        # TODO: Add joystick support
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
            for j in joysticks:
                devices.append(JoystickInput(actions, j))

        if len(devices) == 0:
            raise UndefinedDeviceError(_('Unable to set a control device.'))

        return devices

    '''
    Public methods
    '''

    def on(self, action_name):
        if self._event_driven:
            if self._keyboard_event:
                for device in self._devices:
                    if device.on(action_name, self._keyboard_event):
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
    def event_driven(self):
        return self._event_driven

    @event_driven.setter
    def event_driven(self, value):
        self._event_driven = value
