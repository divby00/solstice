from gettext import gettext as _
import io
import pygame
import xml.etree.cElementTree as ElementTree


class TiledLoaderError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Tileset(object):
    def __init__(self, name, w, h, tilew, tileh, src, firstgid):
        self.name = name
        self.w = w
        self.h = h
        self.tilew = tilew
        self.tileh = tileh
        self.src = src
        self.firstgid = firstgid

    def __cmp__(self, other):
        return cmp(self.firstgid, other.firstgid)


class Tile(object):
    def __init__(self, srfc, size):
        self.srfc = srfc
        self.size = size


class Map(object):
    """
    Contains level and tile sizes.
    """

    def __init__(self, width, height, tilewidth, tileheight, enemy_data):
        self.width = width
        self.height = height
        self.tilewidth = tilewidth
        self.tileheight = tileheight
        self.width_pixels = width * tilewidth
        self.height_pixels = height * tileheight
        self.enemy_data = enemy_data


class Layer(object):
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.data = []
        self.visible = False
        self.hard_tiles = []

    def hard(self, x, y):
        tile = self.get_gid(x, y)

        if tile in self.hard_tiles:
            return True

        return False

    def set_gid(self, x, y, gid):
        self.data[(y * self.size[0]) + x] = gid

    def get_gid(self, x, y):

        if x < 0 or y < 0:
            return 0

        if (y * self.size[0]) + x >= (self.size[0] * self.size[1]):
            return 0

        return self.data[(y * self.size[0]) + x]


class TiledLevel(object):
    LEVELS = 'levels/'
    GFX = 'gfx/'
    WIDTH = 'width'
    HEIGHT = 'height'
    TILEWIDTH = 'tilewidth'
    TILEHEIGHT = 'tileheight'
    TILESET = 'tileset'
    TILE = 'tile'
    NAME = 'name'
    PROPERTIES = 'properties'
    SPECIAL = 'special'
    ZINDEX = 'zindex'
    GID = 'gid'
    DATA = 'data'
    VALUE = 'value'
    LAYER = 'layer'
    IMAGE = 'image'
    SOURCE = 'source'
    START = 'start'
    START_POINT = 'start_point'
    EXIT_POINT = 'exit_point'
    HARD = 'hard'
    ANIMATION = 'animation'
    ID = 'id'
    IMAGELAYER = 'imagelayer'
    FIRSTGID = 'firstgid'

    def __init__(self, zf, xml_data):
        self.layers = []
        self.tiles = []
        self.hard_tiles = []
        self.animated_tiles = {}
        self.items = {}
        self.locks = []
        self.beam_barriers = []
        self.container = None
        self.magnetic_fields = []
        self.nothrust = {}
        self.rails = {}
        self.teleports = {}
        self.zf = zf
        self.start_tile = 0
        self.start_point = None
        self.exit_point = None
        self.__load(xml_data)

    def __load_map_info(self):

        """ Reads global enemy data such as max. number of enemies and enemy frecuency """
        enemy_data = {}

        for properties in self.root.findall('properties'):
            for prop in properties.findall('property'):
                name = prop.get(TiledLevel.NAME)
                value = prop.get(TiledLevel.VALUE)
                enemy_data[name] = value

        return Map(int(self.root.get(TiledLevel.WIDTH)),
                   int(self.root.get(TiledLevel.HEIGHT)),
                   int(self.root.get(TiledLevel.TILEWIDTH)),
                   int(self.root.get(TiledLevel.TILEHEIGHT)),
                   enemy_data)

    def __load_back_info(self):
        source = None
        back = None

        for imagelayer in self.root.findall(TiledLevel.IMAGELAYER):
            if imagelayer.get(TiledLevel.NAME) == 'back':
                for image in imagelayer.findall(TiledLevel.IMAGE):
                    source = image.get(TiledLevel.SOURCE)

        if source is not None:
            img_data = self.zf.read(TiledLevel.GFX + source)
            byte_data = io.BytesIO(img_data)

            if byte_data is not None:
                back = pygame.image.load(byte_data)

        if back is None:
            raise TiledLoaderError(_('Unable to find back layer in level data.'))

        return back

    def __load_animations_info(self):
        found = False
        animated_tiles = {}

        for obj in self.root.findall('objectgroup'):

            if obj.get(TiledLevel.NAME) == TiledLevel.SPECIAL:
                found = True

                for o in obj.findall('object'):
                    objx = o.get('x')
                    objy = o.get('y')
                    animation_name = ''
                    animation_zindex = ''

                    for prop in o.findall('properties'):
                        for p in prop.findall('property'):
                            pname = p.get(TiledLevel.NAME)
                            pvalue = p.get(TiledLevel.VALUE)

                            if pname == TiledLevel.ANIMATION:
                                animation_name = pvalue

                            if pname == TiledLevel.ZINDEX:
                                animation_zindex = pvalue

                            if animation_name is not '' and animation_zindex is not '':
                                animated_tiles.update(
                                    {''.join([animation_zindex, ' ', objx, ' ', objy]): animation_name})

        if not found:
            raise TiledLoaderError(_('Unable to find animations layer in level data.'))

        return animated_tiles

    def __load_special_info(self):
        found = False
        special = {}

        for obj in self.root.findall('objectgroup'):

            if obj.get(TiledLevel.NAME) == TiledLevel.SPECIAL:
                found = True

                for o in obj.findall('object'):
                    objx = o.get('x')
                    objy = o.get('y')
                    objw = o.get('width')
                    objh = o.get('height')

                    properties = {}

                    for prop in o.findall('properties'):
                        for p in prop.findall('property'):
                            pname = p.get(TiledLevel.NAME)
                            pvalue = p.get(TiledLevel.VALUE)
                            properties.update({pname: pvalue})

                    special.update({''.join([objx, ' ', objy, ' ', objw, ' ', objh]): properties})

        if not found:
            raise TiledLoaderError(_('Unable to find special layer in level data.'))

        return special

    @staticmethod
    def __parse_container_info(special):
        for s in special:
            for a in special[s]:
                if a == 'container':
                    return s

    @staticmethod
    def __parse_beam_barriers_info(special):
        beam_barriers = []

        for s in special:
            if 'beam_barrier_locked_by' in special[s]:
                beam_barriers.append(''.join([special[s]['beam_barrier_locked_by'], ' ', s]))

        return beam_barriers

    @staticmethod
    def __parse_locks_info(special):
        locks = []

        for s in special:
            lock_id = None

            for a in special[s]:
                if a == 'lock':
                    lock_id = special[s].get(a)

                if a == 'type':
                    lock_type = special[s].get(a)

                    if lock_id is not None and lock_type is not None:
                        locks.append(''.join([lock_id, ' ', s, ' ', lock_type]))

        return locks

    @staticmethod
    def __parse_teleports_info(special):
        teleports = []

        for s in special:
            teleport_id = None

            for a in special[s]:
                if a == 'teleport':
                    teleport_id = special[s].get(a)

                    if teleport_id is not None:
                        teleports.append(''.join([teleport_id, ' ', s]))

        return teleports

    @staticmethod
    def __parse_rails_info(special):
        rails = []

        for s in special:
            rail = None
            direction = None

            for a in special[s]:
                if a == 'rails':
                    rail = special[s].get(a)

                if a == 'direction':
                    direction = special[s].get(a)

                if rail is not None and direction is not None:
                    rails.append(''.join([s, ' ', direction]))

        return rails

    @staticmethod
    def __parse_magnetic_info(special):
        magnetic_fields = []

        for s in special:
            for a in special[s]:
                if a == 'magnetic':
                    magnetic_fields.append(s)
        return magnetic_fields

    @staticmethod
    def __parse_nothrust_info(special):
        nothrust = []

        for s in special:
            for a in special[s]:
                if a == 'nothrust':
                    nothrust.append(s)
        return nothrust

    @staticmethod
    def __parse_items_info(special):
        items = []

        for s in special:
            item_name = None
            item_unlocks = None

            for a in special[s]:

                if a == 'item':
                    item_name = special[s].get(a)

                if a == 'unlocks':
                    item_unlocks = int(special[s].get(a))

            if item_name is not None:
                items.append(''.join([item_name, ' ', s, ' ', str(item_unlocks)]))

        return items

    @staticmethod
    def _parse_info_areas(special):
        rails = []

        for s in special:
            rail = None
            direction = None

            for a in special[s]:
                if a == 'rails':
                    rail = special[s].get(a)

                if a == 'direction':
                    direction = special[s].get(a)

                if rail is not None and direction is not None:
                    rails.append(''.join([s, ' ', direction]))

        return rails

    def __load_tileset_info(self):
        tilesets = []

        for tileset in self.root.findall(TiledLevel.TILESET):
            tilewidth = int(tileset.get(TiledLevel.TILEWIDTH))
            tileheight = int(tileset.get(TiledLevel.TILEHEIGHT))
            firstgid = int(tileset.get(TiledLevel.FIRSTGID))
            name = tileset.get(TiledLevel.NAME)
            imgwidth = 0
            imgheight = 0

            if 'object' in name:
                continue

            source = None

            for image in tileset.findall(TiledLevel.IMAGE):
                source = image.get(TiledLevel.SOURCE)
                imgwidth = int(image.get(TiledLevel.WIDTH))
                imgheight = int(image.get(TiledLevel.HEIGHT))

            for tile in tileset.findall(TiledLevel.TILE):
                tileid = int(tile.get(TiledLevel.ID))

                for properties in tile.findall(TiledLevel.PROPERTIES):
                    for prop in properties:
                        name = prop.get(TiledLevel.NAME)

                        if name == TiledLevel.HARD:
                            if prop.get(TiledLevel.VALUE) == 'True':
                                self.hard_tiles.append(tileid + firstgid)

            tilesets.append(Tileset(name, imgwidth, imgheight, tilewidth,
                                    tileheight, source, firstgid))

        tilesets.sort(key=lambda obj: obj.firstgid)
        return tilesets

    def __load_tileset_graphics(self):
        # Load sprites for the tiles
        tiles = []
        img_count = 0
        blank = pygame.Color(0, 0, 0, 0)

        for t in self.tilesets:
            img_data = self.zf.read(TiledLevel.GFX + t.src)
            byte_data = io.BytesIO(img_data)

            if byte_data is not None:
                t.img = pygame.image.load(byte_data)
                t.img = t.img.convert_alpha()

                if t.img is not None:

                    for y in xrange(0, t.h, t.tileh):

                        for x in xrange(0, t.w, t.tilew):
                            srfc = pygame.Surface((t.tilew, t.tileh))
                            srfc = srfc.convert_alpha()

                            if srfc is not None:
                                srfc.fill(blank)
                                srfc.blit(t.img,
                                          (0, 0),
                                          (x, y, t.tilew, t.tileh),
                                          0)

                            tiles.append(Tile(srfc, (t.tilew, t.tileh)))
                            img_count += 1

        print('Loaded ' + str(img_count) + ' tiles')
        return tiles

    def __load_layers_info(self):
        layers = []
        layerwidth = layerheight = layername = gid = None

        for layer in self.root.findall(TiledLevel.LAYER):
            layerwidth = int(layer.get(TiledLevel.WIDTH))
            layerheight = int(layer.get(TiledLevel.HEIGHT))
            layername = layer.get(TiledLevel.NAME)

            if layername in ['walls', 'background', 'hard', 'foreground']:

                l = Layer(layername, (layerwidth, layerheight))

                for data in layer.findall(TiledLevel.DATA):
                    for tile in data.findall(TiledLevel.TILE):
                        gid = int(tile.get(TiledLevel.GID))
                        l.data.append(gid)

                layers.append(l)

            else:
                print(_('Skipping layer %s' % layername))
        return layers

    def __get_start_point(self):
        start_point = None
        for obj in self.root.findall('objectgroup'):

            if obj.get(TiledLevel.NAME) == TiledLevel.SPECIAL:
                found = True

                for o in obj.findall('object'):
                    objx = o.get('x')
                    objy = o.get('y')

                    for prop in o.findall('properties'):
                        for p in prop.findall('property'):
                            pname = p.get(TiledLevel.NAME)
                            pvalue = p.get(TiledLevel.VALUE)

                            if pname == TiledLevel.START_POINT:
                                start_point = int(objx), int(objy)

        if not start_point:
            raise TiledLoaderError(_('Unable to find start point in level data.'))

        return start_point

    def __get_exit_point(self):
        exit_point = None
        for obj in self.root.findall('objectgroup'):

            if obj.get(TiledLevel.NAME) == TiledLevel.SPECIAL:
                found = True

                for o in obj.findall('object'):
                    objx = o.get('x')
                    objy = o.get('y')
                    objw = o.get('width')
                    objh = o.get('height')

                    for prop in o.findall('properties'):
                        for p in prop.findall('property'):
                            pname = p.get(TiledLevel.NAME)
                            pvalue = p.get(TiledLevel.VALUE)

                            if pname == TiledLevel.EXIT_POINT:
                                exit_point = int(objx), int(objy), int(objw), int(objh)

        if not exit_point:
            raise TiledLoaderError(_('Unable to find exit point in level data.'))

        return exit_point

    def __load(self, xml_data):
        # XML parsing
        before = pygame.time.get_ticks()
        self.root = ElementTree.fromstring(xml_data)
        after = pygame.time.get_ticks()
        print('\tLEVEL: resources.xml parsed in %d milliseconds.' % (after - before))

        # Read basic map info
        before = pygame.time.get_ticks()
        self.map = self.__load_map_info()
        after = pygame.time.get_ticks()
        print('\tLEVEL: Map loaded in %d milliseconds.' % (after - before))

        # Read tileset info
        before = pygame.time.get_ticks()
        self.tilesets = self.__load_tileset_info()
        self.tiles = self.__load_tileset_graphics()
        after = pygame.time.get_ticks()
        print('\tLEVEL: Tileset info loaded in %d milliseconds.' % (after - before))

        # Read back info. Back info is the first image being rendered.
        before = pygame.time.get_ticks()
        self.back = self.__load_back_info()
        after = pygame.time.get_ticks()
        print('\tLEVEL: Back info loaded in %d milliseconds.' % (after - before))

        # Read animations info
        before = pygame.time.get_ticks()
        self.animated_tiles = self.__load_animations_info()
        after = pygame.time.get_ticks()
        print('\tLEVEL: Animations info loaded in %d milliseconds.' % (after - before))

        # Read special layer info
        before = pygame.time.get_ticks()
        special = self.__load_special_info()
        self.teleports = self.__parse_teleports_info(special)
        self.magnetic_fields = self.__parse_magnetic_info(special)
        self.container_info = self.__parse_container_info(special)
        self.locks = self.__parse_locks_info(special)
        self.beam_barriers = self.__parse_beam_barriers_info(special)
        self.items = self.__parse_items_info(special)
        self.nothrust = self.__parse_nothrust_info(special)
        self.rails = self.__parse_rails_info(special)
        self.info_areas = self._parse_info_areas(special)

        after = pygame.time.get_ticks()
        print('\tLEVEL: Special info loaded in %d milliseconds.' % (after - before))

        # Read layers info
        before = pygame.time.get_ticks()
        self.layers = self.__load_layers_info()
        after = pygame.time.get_ticks()
        print('\tLEVEL: Layers info loaded in %d milliseconds.' % (after - before))

        # Get starting point
        before = pygame.time.get_ticks()
        self.start_point = self.__get_start_point()
        after = pygame.time.get_ticks()
        print('\tLEVEL: Start point info loaded in %d milliseconds.' % (after - before))

        # Get exit point
        before = pygame.time.get_ticks()
        self.exit_point = self.__get_exit_point()
        after = pygame.time.get_ticks()
        print('\tLEVEL: Exit info loaded in %d milliseconds.' % (after - before))

    def get_gid(self, x, y, name):
        for l in self.layers:
            if l.name == name:
                return l.get_gid(x, y)
        return 0

    def is_hard(self, x, y):
        if self.get_gid(x, y, TiledLevel.HARD) in self.hard_tiles:
            return True
        return False

    def is_nothrust(self, x, y):
        if self.get_gid(x, y, TiledLevel.SPECIAL):
            return True
        return False
