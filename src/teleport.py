class Teleport(object):

    INACTIVE = 0
    ACTIVE = 1

    def __init__(self, id, position, size):
        self.id = id
        self.x, self.y = position[0] + 256, position[1] + 144
        self.w, self.h = size
        self.status = Teleport.INACTIVE


class TeleportBuilder(object):

    @staticmethod
    def build(teleports):
        results = []

        for t in teleports:
            teleport_elements = t.split(' ')
            id = int(teleport_elements[0])
            x = int(teleport_elements[1])
            y = int(teleport_elements[2])
            w = int(teleport_elements[3])
            h = int(teleport_elements[4])

            teleport = None
            position = (x, y)
            size = (w, h)
            teleport = Teleport(id, (x, y), (w, h))
            results.append(teleport)
            
        return results
