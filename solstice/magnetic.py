class Magnetic(object):
    def __init__(self, position, size):
        self._position = position[0] + 256, position[1] + 144
        self._size = size

    @property
    def position(self):
        return self._position

    @property
    def size(self):
        return self._size


class MagneticBuilder(object):
    @staticmethod
    def build(magnetic_fields):
        results = []
        for magnetic_field in magnetic_fields:
            magnetic_elements = magnetic_field.split(' ')
            x = int(magnetic_elements[0])
            y = int(magnetic_elements[1])
            w = int(magnetic_elements[2])
            h = int(magnetic_elements[3])
            results.append(Magnetic((x, y), (w, h)))

        return results
