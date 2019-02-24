from gettext import gettext as _

import teleport


class Item(object):
    def __init__(self, game_context, name, position, size, unlocks):
        self._name = name
        self._x, self._y = position[0] + 256, position[1] + 144
        self._w, self._h = size
        self._active = True
        self._sprite = None
        self._unlocks = unlocks
        self._position = position
        self._size = size
        self._game_context = game_context
        self._player = game_context.player
        self._locks = game_context.locks
        self._beam_barriers = game_context.beam_barriers
        self._teleports = game_context.teleports
        self._container = game_context.container

    '''
    Private methods
    '''

    def __repr__(self):
        return ''.join([self._name, str(self._position), str(self._size)])

    '''
    Public methods
    '''

    def run(self):
        raise NotImplementedError('Implement this method')

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
    def sprite(self):
        return self._sprite

    @property
    def name(self):
        return self._name

    @property
    def unlocks(self):
        return self._unlocks


class ItemUnlocker(Item):
    def __init__(self, game_context, name, position, size, unlocks):
        super(ItemUnlocker, self).__init__(game_context, name, position, size, unlocks)

    '''
    Public methods
    '''

    def run(self):
        x = self._player.x
        y = self._player.y

        # Check if player is near a lock
        for lock in self._locks:
            if x + 8 >= lock.x - 8 and x - 8 <= lock.x + lock.w + 8 \
                    and y + 8 >= lock.y - 8 and y - 8 <= lock.y + lock.h + 8:

                # Check if selected_item unlocks the nearby lock
                if self._player.selected_item.unlocks == lock.lock_id:

                    # Open the lock
                    self._game_context.get_renderer().change_animation((lock.x, lock.y), None)

                    # Remove hard zones
                    for layer in self._game_context.get_layers():
                        if layer.name == 'hard':
                            gx = (lock.x - 256) / 8
                            gy = (lock.y - 144) / 8
                            gw = lock.w / 8
                            gh = lock.h / 8

                            for a in xrange(gy, gy + gh):
                                for i in xrange(gx, gx + gw):
                                    layer.set_gid(i, a, 0)

                    # Delete item
                    self._player.selected_item = None

                    # Generate explosion particles
                    exp_particles = self._game_context.particles_manager.get('exp')
                    exp_particles.generate((lock.x, lock.x + lock.w, lock.y, lock.y + lock.h))
                    self._game_context.sound_player.play_sample('exp')


class ItemFuse(ItemUnlocker):
    def __init__(self, game_context, position, size, unlocks):
        super(ItemFuse, self).__init__(game_context, 'fuse', position, size, unlocks)

    '''
    Public methods
    '''

    def run(self):
        x = self._player.x
        y = self._player.y

        # Check if player is near a lock
        for lock in self._locks:
            if x + 8 >= lock.x - 8 and x - 8 <= lock.x + lock.w + 8 \
                    and y + 8 >= lock.y - 8 and y - 8 <= lock.y + lock.h + 8:

                # Check if selected_item unlocks the nearby lock
                if self._player.selected_item.unlocks == lock.id:

                    # Change sprite for fuse box
                    self._game_context.get_renderer().change_animation((lock.x, lock.y),
                                                                       'object014')

                    # Remove beam barrier
                    for barrier in self._beam_barriers:
                        if barrier.locked_by == lock.id:

                            # Remove beam barrier animation
                            for y in xrange(barrier.y, barrier.y + barrier.h):
                                self._game_context.get_renderer().change_animation((barrier.x, y),
                                                                                   None)

                            # Remove hard zones
                            hard_layer = [layer for layer in self._game_context.get_layers()
                                          if layer.name == 'hard'][0]
                            if hard_layer:
                                gx, gy = (barrier.x - 256) / 8, (barrier.y - 144) / 8
                                gw, gh = barrier.w / 8, barrier.h / 8

                                for a in xrange(gy, gy + gh):
                                    for i in xrange(gx, gx + gw):
                                        hard_layer.set_gid(i, a, 0)

                    # Delete item
                    self._player.selected_item = None


class ItemBomb(Item):
    def __init__(self, game_context, position, size):
        super(ItemBomb, self).__init__(game_context, 'bomb', position, size, None)

    '''
    Public methods
    '''

    def run(self):
        pass


class ItemBarrel(Item):
    def __init__(self, game_context, position, size):
        super(ItemBarrel, self).__init__(game_context, 'barrel', position, size, None)

    '''
    Public methods
    '''

    def run(self):
        self._player.thrust = 107
        self._player.selected_item = None


class ItemBattery(Item):
    def __init__(self, game_context, position, size):
        super(ItemBattery, self).__init__(game_context, 'battery', position, size, None)

    '''
    Public methods
    '''

    def run(self):
        self._player.bullets = 107
        self._player.selected_item = None


class ItemCard(Item):
    def __init__(self, game_context, position, size, card_id):
        super(ItemCard, self).__init__(game_context, ''.join(['card', card_id]), position, size,
                                       None)
        self.card_id = card_id
        self.exit_point = game_context.exit_point
        self._game_context = game_context

    '''
    Public methods
    '''

    def run(self):
        pass


class ItemDrill(ItemUnlocker):
    def __init__(self, game_context, position, size, unlocks):
        super(ItemDrill, self).__init__(game_context, 'drill', position, size, unlocks)

    '''
    Public methods
    '''

    def run(self):
        super(ItemDrill, self).run()


class ItemKey(ItemUnlocker):
    def __init__(self, game_context, position, size, unlocks):
        super(ItemKey, self).__init__(game_context, 'key', position, size, unlocks)

    '''
    Public methods
    '''

    def run(self):
        super(ItemKey, self).run()


class ItemTeleport(Item):
    def __init__(self, game_context, position, size):
        super(ItemTeleport, self).__init__(game_context, 'teleport_pass', position, size, None)

    '''
    Public methods
    '''

    def run(self):
        x = self._player.x
        y = self._player.y

        # Check if player is near a teleport machine, in that case prepare both teleport machines
        # preventing to use a teleporter key with an already activated teleporter
        for telport in self._teleports:
            if x + 8 >= telport.x - 8 and x - 8 <= telport.x + telport.w + 16 \
                    and y + 8 >= telport.y - 8 and y - 8 <= telport.y + telport.h + 8 \
                    and telport.status == teleport.Teleport.INACTIVE:
                telport.status = teleport.Teleport.ACTIVE

                for tel in self._teleports:
                    if tel.teleport_id == telport.teleport_id \
                            and (tel.x != telport.x or tel.y != telport.y):
                        tel.status = teleport.Teleport.ACTIVE
                        self._player.teleport_destiny = tel
                        self._change_teleporters_animation(telport, tel, 'object017')
                    if tel.teleport_id == telport.teleport_id \
                            and tel.x == telport.x and tel.y == telport.y:
                        tel.status = teleport.Teleport.ACTIVE
                        self._player.teleport_source = tel
                        self._change_teleporters_animation(telport, tel, 'object017')

                self._player.selected_item = None

    def _change_teleporters_animation(self, source_teleporter, destiny_teleporter, animation_name):
        '''
        Teleporter coordinates need to be transformed to the animation coordinates, therefore the -16 and -24
        sustraction. This method returns the coordinates for the paired teleports.
        '''
        self._game_context._renderer_object.change_animation(
            (source_teleporter.x - 16, source_teleporter.y - 24), animation_name)
        self._game_context._renderer_object.change_animation(
            (destiny_teleporter.x - 16, destiny_teleporter.y - 24), animation_name)


class ItemTnt(ItemUnlocker):
    def __init__(self, game_context, position, size, unlocks):
        super(ItemTnt, self).__init__(game_context, 'tnt', position, size, unlocks)

    '''
    Public methods
    '''

    def run(self):
        super(ItemTnt, self).run()


class ItemDetonator(ItemUnlocker):
    def __init__(self, game_context, position, size, unlocks):
        super(ItemDetonator, self).__init__(game_context, 'detonator', position, size, unlocks)

    '''
    Public methods
    '''

    def run(self):
        super(ItemDetonator, self).run()


class ItemWaste(Item):
    def __init__(self, game_context, position, size):
        super(ItemWaste, self).__init__(game_context, 'waste', position, size, None)

    '''
    Public methods
    '''

    def run(self):
        # Check if player is close to the nuclear waste container
        if self._player.x - 264 + 8 >= self._container.x \
                and self._player.x - 264 - 8 <= self._container.x + self._container.w \
                and self._player.y - 152 - 8 <= self._container.y + self._container.h \
                and self._player.y - 152 + 8 >= self._container.y:
            self._container.secured = True
            self._player.selected_item = None
            self._game_context.sound_player.play_sample('secured')


class UnknownItemError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class ItemBuilder(object):
    @staticmethod
    def build(game_context, resourcemanager, items):

        results = []

        for i in items:
            item_elements = i.split(' ')
            item_name = item_elements[0]
            item_x = int(item_elements[1])
            item_y = int(item_elements[2])
            item_w = int(item_elements[3])
            item_h = int(item_elements[4])

            if item_name not in ['barrel', 'battery', 'drill', 'key',
                                 'teleport_pass', 'tnt', 'waste', 'bomb', 'fuse', 'detonator'] \
                    and not item_name.startswith('card'):
                raise UnknownItemError(_('Unable to build %s item') % item_name)

            item = None
            position = (item_x, item_y)
            size = (item_w, item_h)

            if item_name == 'barrel':
                item = ItemBarrel(game_context, position, size)

            if item_name == 'battery':
                item = ItemBattery(game_context, position, size)

            if item_name == 'bomb':
                item = ItemBomb(game_context, position, size)

            if item_name == 'fuse':
                item = ItemFuse(game_context, position, size, item_elements[5])

            if item_name.startswith('card'):
                card_id = item_name[-2:]
                item = ItemCard(game_context, position, size, card_id)

            if item_name == 'drill':
                item = ItemDrill(game_context, position, size, item_elements[5])

            if item_name == 'key':
                item = ItemKey(game_context, position, size, item_elements[5])

            if item_name == 'teleport_pass':
                item = ItemTeleport(game_context, position, size)

            if item_name == 'tnt':
                item = ItemTnt(game_context, position, size, item_elements[5])

            if item_name == 'detonator':
                item = ItemDetonator(game_context, position, size, item_elements[5])

            if item_name == 'waste':
                item = ItemWaste(game_context, position, size)

            sprite = ''.join(['item_', item_name])
            item._sprite = resourcemanager.get(sprite)
            results.append(item)

        return results
