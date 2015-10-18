from gettext import gettext as _

import teleport


class Item(object):
    def __init__(self, game_context, name, position, size, unlocks):
        self.name = name
        self.x, self.y = position[0] + 256, position[1] + 144
        self.w, self.h = size
        self.active = True
        self.sprite = None
        self.unlocks = unlocks
        self.game_context = game_context
        self.player = game_context.player
        self.locks = game_context.locks
        self.teleports = game_context.teleports

    def run(self):
        raise NotImplementedError('Implement this method')

    def __repr__(self):
        object_name = ''.join([self.name, str(self.position), str(self.size)])
        return object_name


class ItemUnlocker(Item):
    def __init__(self, game_context, name, position, size, unlocks):
        super(ItemUnlocker, self).__init__(game_context, name, position, size, unlocks)

    def run(self):
        x = self.player.x
        y = self.player.y
        w = self.player.w
        h = self.player.h

        # Check if player is near a lock
        for l in self.locks:
            if x + 8 >= l.x - 8 and x - 8 <= l.x + l.w + 8 and y + 8 >= l.y - 8 and y - 8 <= l.y + l.h + 8:

                # Check if selected_item unlocks the nearby lock
                if self.player.selected_item.unlocks == l.id:

                    # Open the lock
                    self.game_context.get_renderer().change_animation((l.x, l.y), None)

                    # Remove hard zones
                    for la in self.game_context.get_layers():
                        if la.name == 'hard':
                            gx = (l.x - 256) / 8
                            gy = (l.y - 144) / 8
                            gw = l.w / 8
                            gh = l.h / 8

                            for a in xrange(gy, gy + gh):
                                for i in xrange(gx, gx + gw):
                                    la.set_gid(i, a, 0)

                    # Delete item
                    self.player.selected_item = None

                    # Generate explosion particles
                    exp_particles = self.game_context.particlesmanager.get('exp')
                    exp_particles.generate((l.x, l.x + l.w, l.y, l.y + l.h))
                    self.game_context.exp.play()


class ItemBomb(Item):
    def __init__(self, game_context, position, size):
        super(ItemBomb, self).__init__(game_context, 'bomb', position, size, None)

    def run(self):
        pass


class ItemBarrel(Item):
    def __init__(self, game_context, position, size):
        super(ItemBarrel, self).__init__(game_context, 'barrel', position, size, None)

    def run(self):
        self.player.thrust = 107
        self.player.selected_item = None


class ItemBattery(Item):
    def __init__(self, game_context, position, size):
        super(ItemBattery, self).__init__(game_context, 'battery', position, size, None)

    def run(self):
        self.player.bullets = 107
        self.player.selected_item = None


class ItemCard(Item):
    def __init__(self, game_context, position, size, card_id):
        super(ItemCard, self).__init__(game_context, ''.join(['card', card_id]), position, size, None)
        self.card_id = card_id

    def run(self):
        pass


class ItemDrill(ItemUnlocker):
    def __init__(self, game_context, position, size, unlocks):
        super(ItemDrill, self).__init__(game_context, 'drill', position, size, unlocks)

    def run(self):
        super(ItemDrill, self).run()


class ItemKey(ItemUnlocker):
    def __init__(self, game_context, position, size, unlocks):
        super(ItemKey, self).__init__(game_context, 'key', position, size, unlocks)

    def run(self):
        super(ItemKey, self).run()


class ItemTeleport(Item):
    def __init__(self, game_context, position, size):
        super(ItemTeleport, self).__init__(game_context, 'teleport_pass', position, size, None)

    def run(self):
        x = self.player.x
        y = self.player.y
        w = self.player.w
        h = self.player.h

        # Check if player is near a teleport machine, in that case prepare both teleport machines
        for t in self.teleports:
            if x + 8 >= t.x - 8 and x - 8 <= t.x + t.w + 16 and y + 8 >= t.y - 8 and y - 8 <= t.y + t.h + 8:
                t.status = teleport.Teleport.ACTIVE

                for destiny in self.teleports:
                    if destiny.id == t.id and (destiny.x != t.x or destiny.y != t.y):
                        destiny.status = teleport.Teleport.ACTIVE
                        self.player.destiny = destiny

                self.player.selected_item = None


class ItemTnt(ItemUnlocker):
    def __init__(self, game_context, position, size, unlocks):
        super(ItemTnt, self).__init__(game_context, 'tnt', position, size, unlocks)

    def run(self):
        super(ItemTnt, self).run()


class ItemWaste(Item):
    def __init__(self, game_context, position, size):
        super(ItemWaste, self).__init__(game_context, 'waste', position, size, None)

    def run(self):
        pass


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

            if item_name not in ['barrel', 'battery', 'drill', 'key', 'teleport_pass', 'tnt', 'waste', 'bomb'] and not \
                    item_name.startswith('card'):
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

            if item_name == 'waste':
                item = ItemWaste(game_context, position, size)

            sprite = ''.join(['item_', item_name])
            print('Sprite:' + sprite)
            item.sprite = resourcemanager.get(sprite)
            results.append(item)

        return results
