class Lock(object):
    def __init__(self, lock_id, position, size, lock_type):
        self._lock_id = lock_id
        self._x, self._y = position[0] + 256, position[1] + 144
        self._w, self._h = size
        self._active = True
        self._lock_type = lock_type

    '''
    Public methods
    '''

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        self._h = value

    @property
    def lock_id(self):
        return self._lock_id


class BeamBarrier(object):
    def __init__(self, locked_by, position, size):
        self._locked_by = locked_by
        self._x, self._y = position[0] + 256, position[1] + 144
        self._w, self._h = size


class BeamBarriersBuilder(object):
    @staticmethod
    def build(beam_barriers):
        results = []
        for beam_barrier in beam_barriers:
            beam_elements = beam_barrier.split(' ')
            locked_by = beam_elements[0]
            x = int(beam_elements[1])
            y = int(beam_elements[2])
            w = int(beam_elements[3])
            h = int(beam_elements[4])
            results.append(BeamBarrier(locked_by, (x, y), (w, h)))

        return results


class LockBuilder(object):
    @staticmethod
    def build(game_context, locks):
        results = []
        for lock in locks:
            lock_elements = lock.split(' ')
            lock_id = lock_elements[0]
            x = int(lock_elements[1])
            y = int(lock_elements[2])
            w = int(lock_elements[3])
            h = int(lock_elements[4])
            lock_type = lock_elements[5]
            results.append(Lock(lock_id, (x, y), (w, h), lock_type))

        # Rebuild hard tiles destroyed when player unlocks some gate.
        for layer in game_context.current_level.layers:
            if layer.name == 'hard':
                for lock in results:
                    gx = (lock.x - 256) / 8
                    gy = (lock.y - 144) / 8
                    gw = lock.w / 8
                    gh = lock.h / 8

                    for a in xrange(gy, gy + gh):
                        for i in xrange(gx, gx + gw):
                            layer.set_gid(i, a, game_context.current_level.hard_tiles[0])

        return results
