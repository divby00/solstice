from gettext import gettext as _
import pygame


class ControlAction(object):
    def __init__(self, name, mapping):
        self.name = name
        self.mapping = mapping


class ControlInput(object):
    def __init__(self, actions):
        self.__register_actions(actions)

    def __register_actions(self, actions):
        self.actions = actions

    def update(self):
        raise NotImplementedError('Not yet implemented')

    def on(self, control_action):
        raise NotImplementedError('Not yet implemented')


class KeyboardInput(ControlInput):
    def __init__(self, actions):
        super(KeyboardInput, self).__init__(actions)
        self.actions = actions
        self.keys = None

    def update(self):
        self.keys = pygame.key.get_pressed()

    def on(self, action_name):
        for a in self.actions:
            if a.name == action_name:
                if self.keys[a.mapping]:
                    return True
        return False


class JoystickInput(ControlInput):
    def __init__(self, actions, joystick):
        super(JoystickInput, self).__init__(actions)
        self.actions = actions
        self.joystick = joystick
        self.joystick.init()

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

    def __init__(self, context):
        self.cfg = context.cfg
        joysticks = [pygame.joystick.Joystick(j) for j in range(pygame.joystick.get_count())]
        self.devices = self.__register_devices(joysticks)

    def __register_devices(self, joysticks):
        devices = []
        actions = []

        if self.cfg.control_type in ['autodetect', 'keyboard']:
            actions.append(ControlAction(Control.UP, self.cfg.key_up))
            actions.append(ControlAction(Control.DOWN, self.cfg.key_down))
            actions.append(ControlAction(Control.LEFT, self.cfg.key_left))
            actions.append(ControlAction(Control.RIGHT, self.cfg.key_right))
            actions.append(ControlAction(Control.ACTION1, self.cfg.key_act1))
            actions.append(ControlAction(Control.ACTION2, self.cfg.key_act2))
            devices.append(KeyboardInput(actions))

        if self.cfg.control_type in ['autodetect', 'joystick']:
            for j in joysticks:
                devices.append(JoystickInput(actions, j))

        if len(devices) == 0:
            raise UndefinedDeviceError(_('Unable to set a control device.'))

        return devices

    def on(self, action_name):
        pygame.event.pump()

        for d in self.devices:
            d.update()

            if d.on(action_name):
                return True
        return False
