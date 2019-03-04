class Crusher(object):

    def __init__(self, position, size):
        self._x, self._y = position[0] + 256, position[1] + 144
        self._w, self._h = size

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


class CrusherBuilder(object):
    @staticmethod
    def build(crushers):
        results = []
        for crusher in crushers:
            crusher_elements = crusher.split(' ')
            x = int(crusher_elements[0])
            y = int(crusher_elements[1])
            w = int(crusher_elements[2])
            h = int(crusher_elements[3])
            results.append(Crusher((x, y), (w, h)))

        return results
