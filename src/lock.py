class Lock(object):
    def __init__(self, game_context, id, position, size):
        self.id = id
        self.x, self.y = position[0] + 256, position[1] + 144
        self.w, self.h = size
        self.active = True


class LockBuilder(object):
    @staticmethod
    def build(game_context, resourcemanager, locks):

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
            lock = Lock(game_context, id, (x, y), (w, h))
            results.append(lock)

        # Rebuild hard tiles destroyed when player unlocks some gate.
        for la in game_context.current_level.layers:
            if la.name == 'hard':
                for l in results:
                    gx = (l.x - 256) / 8
                    gy = (l.y - 144) / 8
                    gw = l.w / 8
                    gh = l.h / 8

                    for a in xrange(gy, gy + gh):
                        for i in xrange(gx, gx + gw):
                            la.set_gid(i, a, game_context.current_level.hard_tiles[0])

        return results
