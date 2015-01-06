from gettext import gettext as _


class Item(object):

    def __init__(self, position, size):
        self.position = position
        self.size = size
        self.active = True
        self.name = None

    def run(self):
        print('No llamar')

    def __str__(self):
        return ''.join(self.name, self.position, self.size)


class ItemBarrel(Item):

    def __init__(self, position, size):
        super(ItemBarrel, self).__init__(position, size)
        self.name = 'barrel'

    def run(self):
        print('Barrel beh')


class ItemBattery(Item):
    
    def __init__(self, position, size):
        super(ItemBattery, self).__init__(position, size)

    def run(self):
        pass


class ItemU(Item):
    
    def __init__(self, position, size):
        super(ItemU, self).__init__(position, size)

    def run(self):
        pass


class ItemDrill(Item):

    def __init__(self, position, size):
        super(ItemDrill, self).__init__(position, size)
        self.name = 'drill'

    def run(self):
        print('My behaviour')


class ItemKey(Item):

    def __init__(self, position, size):
        super(ItemKey, self).__init__(position, size)
        self.name = 'key'

    def run(self):
        print('My behaviour')


class ItemTeleport(Item):
    
    def __init__(self, position, size):
        super(ItemTeleport, self).__init__(position, size)

    def run(self):
        pass


class ItemTnt(Item):
    
    def __init__(self, position, size):
        super(ItemTnt, self).__init__(position, size)

    def run(self):
        pass


class ItemWaste(Item):
    
    def __init__(self, position, size):
        super(ItemWaste, self).__init__(position, size)

    def run(self):
        pass


class UnknownItemError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class ItemBuilder(object):

    @staticmethod
    def build(name, position, size):

        if name == 'barrel':
            return ItemBarrel(position, size)

        if name == 'battery':
            return ItemBattery(position, size)

        if name == 'drill':
            return ItemDrill(position, size)

        if name == 'key':
            return ItemKey(position, size)

        if name == 'teleport':
            return ItemTeleport(position, size)

        if name == 'tnt':
            return ItemTnt(position, size)

        if name == 'waste':
            return ItemWaste(position, size)

        raise UnknownItemError(_('Unable to build %s item' % name))
