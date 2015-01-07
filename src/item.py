from gettext import gettext as _


class Item(object):

    def __init__(self, name, position, size, unlocks):
        self.name = name
        self.x, self.y = position[0] + 256, position[1] + 144
        self.w, self.h = size
        self.unlocks = unlocks
        self.active = True
        self.sprite = None

    def run(self):
        raise NotImplementedError('Implement this method')

    def __repr__(self):
        object_name = ''.join([self.name, str(self.position), str(self.size)])
        return object_name


class ItemBarrel(Item):

    def __init__(self, position, size, unlocks):
        super(ItemBarrel, self).__init__('barrel', position, size, unlocks)

    def run(self):
        print('Barrel beh')


class ItemBattery(Item):
    
    def __init__(self, position, size, unlocks):
        super(ItemBattery, self).__init__('battery', position, size, unlocks)

    def run(self):
        pass


class ItemU(Item):
    
    def __init__(self, position, size, unlocks):
        super(ItemU, self).__init__('U', position, size, unlocks)

    def run(self):
        pass


class ItemDrill(Item):

    def __init__(self, position, size, unlocks):
        super(ItemDrill, self).__init__('drill', position, size, unlocks)

    def run(self):
        pass


class ItemKey(Item):

    def __init__(self, position, size, unlocks):
        super(ItemKey, self).__init__('key', position, size, unlocks)

    def run(self):
        pass


class ItemTeleport(Item):
    
    def __init__(self, position, size, unlocks):
        super(ItemTeleport, self).__init__('teleport_pass', position, size, unlocks)

    def run(self):
        pass


class ItemTnt(Item):
    
    def __init__(self, position, size, unlocks):
        super(ItemTnt, self).__init__('tnt', position, size, unlocks)

    def run(self):
        pass


class ItemWaste(Item):
    
    def __init__(self, position, size, unlocks):
        super(ItemWaste, self).__init__('waste', position, size, unlocks)

    def run(self):
        pass


class UnknownItemError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class ItemBuilder(object):

    @staticmethod
    def build(resourcemanager, items):

        results = []

        for i in items:
            item_elements = i.split(' ')
            item_name = item_elements[0]
            item_x = int(item_elements[1])
            item_y = int(item_elements[2])
            item_w = int(item_elements[3])
            item_h = int(item_elements[4])
            item_unlocks = item_elements[5]

            if item_name not in ['barrel', 'battery', 'drill', 'key',
                                 'teleport_pass', 'tnt', 'waste']:
                raise UnknownItemError(_('Unable to build %s item') % item_name)

            item = None
            position = (item_x, item_y)
            size = (item_w, item_h)
            unlocks = item_unlocks

            if item_name == 'barrel':
                item = ItemBarrel(position, size, unlocks)

            if item_name == 'battery':
                item = ItemBattery(position, size, unlocks)

            if item_name == 'drill':
                item = ItemDrill(position, size, unlocks)

            if item_name == 'key':
                item = ItemKey(position, size, unlocks)

            if item_name == 'teleport_pass':
                item = ItemTeleport(position, size, unlocks)

            if item_name == 'tnt':
                item = ItemTnt(position, size, unlocks)

            if item_name == 'waste':
                item = ItemWaste(position, size, unlocks)

            sprite = ''.join(['item_', item_name])
            item.sprite = resourcemanager.get(sprite)
            results.append(item)

        return results
