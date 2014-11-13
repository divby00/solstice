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

    def update(self):
        pass

    def on(self):
        pass


class JoystickInput(ControlInput):

    def __init__(self, actions, joystick):
        super(JoystickInput, self).__init__(actions)
        self.joystick = joystick
        self.joystick.init()

    def update(self):
        pass

    def on(self):
        pass


class UndefinedDeviceError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Control(object):

    def __init__(self, context):
        self.cfg = context.cfg
        joysticks = [pygame.joystick.Joystick(j) for j in range(pygame.joystick.get_count())]
        self.devices = self.__register_devices(joysticks)

    def __register_devices(self, joysticks):
        devices = []
        actions = []
        actions.append(ControlAction('up', 0))
        actions.append(ControlAction('down', 1))
        actions.append(ControlAction('left', 2))
        actions.append(ControlAction('right', 3))

        if self.cfg.control_type in ['autodetect', 'keyboard']:
            devices.append(KeyboardInput(actions))

        if self.cfg.control_type in ['autodetect', 'joystick']:
            for j in range(joysticks):
                devices.append(JoystickInput(actions, joysticks[j]))

        if len(devices) == 0:
            raise UndefinedDeviceError(_('Unable to set a control device.'))

        return devices
