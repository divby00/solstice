from enum import Enum


class CrusherStatus(Enum):
    relaxed = 0,
    crushing_first = 1,
    crushing_second = 2,
    crushing_third = 3


class Crusher(object):

    def __init__(self, id, position, size):
        self._id = id
        self._x, self._y = position[0] + 256, position[1] + 144
        self._w, self._h = size
        self._active_counter = 0
        self._status = CrusherStatus.relaxed

    def run(self):
        pass

    @property
    def id(self):
        return self._id

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
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        if self._status == CrusherStatus.relaxed:
            self._h = 24
        elif self._status == CrusherStatus.crushing_first:
            self._h = 32
        elif self._status == CrusherStatus.crushing_second:
            self._h = 40
        elif self._status == CrusherStatus.crushing_third:
            self._h = 48

    @property
    def active_counter(self):
        return self._active_counter

    @active_counter.setter
    def active_counter(self, value):
        self._active_counter = value


class CrusherBuilder(object):
    @staticmethod
    def build(crushers):
        results = []

        for crusher in crushers:
            crusher_elements = crusher.split(' ')
            id = int(crusher_elements[0])
            x = int(crusher_elements[1])
            y = int(crusher_elements[2])
            w = int(crusher_elements[3])
            h = int(crusher_elements[4])
            results.append(Crusher(id, (x, y), (w, h)))

        return results
