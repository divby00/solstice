class LifeExchanger(object):

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


class LifeExchangerBuilder(object):
    @staticmethod
    def build(life_exchangers):
        results = []
        for life_exchanger in life_exchangers:
            life_exchanger_elements = life_exchanger.split(' ')
            x = int(life_exchanger_elements[0])
            y = int(life_exchanger_elements[1])
            w = int(life_exchanger_elements[2])
            h = int(life_exchanger_elements[3])
            results.append(LifeExchanger((x, y), (w, h)))

        return results
