# -*- coding: utf-8 -*-

from enum import IntEnum


class CrusherStatus(IntEnum):
    RELAXED = 0,
    FIRST = 1,
    SECOND = 2,
    THIRD = 3


class CrusherThreshold(IntEnum):
    SLOW = 8,
    QUICK = 2


class CrusherDirection(IntEnum):
    UP = -1,
    DOWN = 1


class CrusherSprites(object):

    def __init__(self, frames):
        self._frames = frames

    @property
    def frames(self):
        return self._frames


class CrusherBuilder(object):
    @staticmethod
    def build(game_context):
        results = []
        sprites = CrusherSprites([game_context.resource_manager.get('crusher0' + str(i)) for i in range(0, 4)])

        for crusher in game_context.current_level.crushers:
            crusher_elements = crusher.split(' ')
            id = int(crusher_elements[0])
            x = int(crusher_elements[1])
            y = int(crusher_elements[2])
            w = int(crusher_elements[3])
            h = int(crusher_elements[4])
            results.append(Crusher(id, (x, y), (w, h), sprites))

        return results


class Crusher(object):

    def __init__(self, id, position, size, sprites):
        self._id = id
        self._x, self._y = position[0] + 256, position[1] + 144
        self._sprites = sprites
        self._w, self._h = size
        self._status_counter = 0
        self._status = CrusherStatus.RELAXED
        self._vertical_direction = CrusherDirection.DOWN
        self._status_threshold = CrusherThreshold.QUICK

    def run(self):
        if self._status_counter % self._status_threshold == 0:
            self._status = self._status + self._vertical_direction

            if self._status > CrusherStatus.THIRD:
                self._status = CrusherStatus.THIRD
                self._status_threshold = CrusherThreshold.SLOW
                self._vertical_direction = CrusherDirection.UP
                self._status_counter = 0

            if self._status < CrusherStatus.RELAXED:
                self._status = CrusherStatus.RELAXED
                self._status_threshold = CrusherThreshold.QUICK
                self._vertical_direction = CrusherDirection.DOWN
                self._status_counter = 0

        self._status_counter = self._status_counter + 1

    def render(self, screen):
        screen.blit(self._sprites.frames[self._status], (self._x, self._y))

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
        if self._status == CrusherStatus.RELAXED:
            self._h = 24
        elif self._status == CrusherStatus.FIRST:
            self._h = 32
        elif self._status == CrusherStatus.SECOND:
            self._h = 40
        elif self._status == CrusherStatus.THIRD:
            self._h = 48
