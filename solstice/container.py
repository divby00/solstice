# -*- coding: utf-8 -*-


class Container(object):

    def __init__(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._secured = False

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
    def secured(self):
        return self._secured

    @secured.setter
    def secured(self, value):
        self._secured = value


class ContainerBuilder(object):

    @staticmethod
    def build(container_info):
        info = container_info.split(' ')
        return Container(int(info[0]), int(info[1]), int(info[2]), int(info[3]))
