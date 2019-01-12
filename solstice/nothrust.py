class NoThrust(object):
    def __init__(self, position, size):
        self._position = position[0] + 256, position[1] + 144
        self._size = size

    @property
    def position(self):
        return self._position

    @property
    def size(self):
        return self._size


class NoThrustBuilder(object):
    @staticmethod
    def build(nothrust_zones):
        results = []
        for no_thrust_zone in nothrust_zones:
            nothrust_zones = no_thrust_zone.split(' ')
            x = int(nothrust_zones[0])
            y = int(nothrust_zones[1])
            w = int(nothrust_zones[2])
            h = int(nothrust_zones[3])
            results.append(NoThrust((x, y), (w, h)))

        return results
