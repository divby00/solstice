class Rails(object):
    def __init__(self, position, size, direction):
        self.position = position[0] + 256, position[1] + 144
        self.size = size
        self.direction = direction


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
            position = (x, y)
            size = (w, h)
            rail_field = None
            rail_field = Rails(position, size, direction)
            results.append(rail_field)

        return results
