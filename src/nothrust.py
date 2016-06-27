class NoThrust(object):
    def __init__(self, position, size):
        self.position = position[0] + 256, position[1] + 144
        self.size = size


class NoThrustBuilder(object):
    @staticmethod
    def build(nothrust):
        results = []

        for m in nothrust:
            nothrust = m.split(' ')
            x = int(nothrust[0])
            y = int(nothrust[1])
            w = int(nothrust[2])
            h = int(nothrust[3])

            nothrust_field = None
            position = (x, y)
            size = (w, h)
            nothrust_field = NoThrust(position, size)

            print('Nothrust')
            print(nothrust_field.position)
            print(nothrust_field.size)
            results.append(nothrust_field)

        return results
