class Rails(object):
    def __init__(self, position, size, direction):
        self._position = position[0] + 256, position[1] + 144
        self._size = size
        self._direction = direction

    @property
    def position(self):
        return self._position

    @property
    def size(self):
        return self._size

    @property
    def direction(self):
        return self._direction


class RailsBuilder(object):
    @staticmethod
    def build(rails):
        results = []
        for rail in rails:
            rail_data = rail.split(' ')
            x = int(rail_data[0])
            y = int(rail_data[1])
            w = int(rail_data[2])
            h = int(rail_data[3])
            direction = int(rail_data[4])
            results.append(Rails((x, y), (w, h), direction))

        return results
