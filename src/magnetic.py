class Magnetic(object):
    def __init__(self, position, size):
        self.position = position[0] + 256, position[1] + 144
        self.size = size


class MagneticBuilder(object):
    @staticmethod
    def build(magnetic_fields):
        results = []

        for m in magnetic_fields:
            magnetic_elements = m.split(' ')
            x = int(magnetic_elements[0])
            y = int(magnetic_elements[1])
            w = int(magnetic_elements[2])
            h = int(magnetic_elements[3])

            magnetic_field = None
            position = (x, y)
            size = (w, h)
            magnetic_field = Magnetic((x, y), (w, h))
            results.append(magnetic_field)

        return results
