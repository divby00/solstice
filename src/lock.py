class Lock(object):

    def __init__(self, id, position, size):
        self.id = id
        self.x, self.y = position[0] + 256, position[1] + 144
        self.w, self.h = size
        self.active = True


class LockBuilder(object):

    @staticmethod
    def build(resourcemanager, locks):

        results = []

        for l in locks:
            lock_elements = l.split(' ')
            id = lock_elements[0]
            x = int(lock_elements[1])
            y = int(lock_elements[2])
            w = int(lock_elements[3])
            h = int(lock_elements[4])

            lock = None
            position = (x, y)
            size = (w, h)
            lock = Lock(id, (x, y), (w, h))
            results.append(lock)

        return results
