class Teleport(object):
    INACTIVE = 0
    ACTIVE = 1

    def __init__(self, teleport_id, position, size):
        self._teleport_id = teleport_id
        self._x, self._y = position[0] + 256, position[1] + 144
        self._w, self._h = size
        self._status = Teleport.INACTIVE

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h

    @property
    def teleport_id(self):
        return self._teleport_id

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value


class TeleportBuilder(object):
    @staticmethod
    def build(teleports):
        results = []
        for telport in teleports:
            teleport_elements = telport.split(' ')
            teleport_id = int(teleport_elements[0])
            x = int(teleport_elements[1])
            y = int(teleport_elements[2])
            w = int(teleport_elements[3])
            h = int(teleport_elements[4])
            results.append(Teleport(teleport_id, (x, y), (w, h)))
        return results
