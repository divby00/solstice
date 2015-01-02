from gettext import gettext as _
import io
import pygame
import xml.etree.ElementTree as ElementTree


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
    '''
    Contains level and tile sizes.
    '''
    def __init__(self, width, height, tilewidth, tileheight):
        self.width = width
        self.height = height
        self.tilewidth = tilewidth
        self.tileheight = tileheight
        self.width_pixels = width * tilewidth
        self.height_pixels = height * tileheight


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
        self.zf = zf
        self.start_tile = 0
        self.start_point = None
        self.__load(xml_data)

    def __load_map_info(self):
       return Map(int(self.root.get(TiledLevel.WIDTH)),
                  int(self.root.get(TiledLevel.HEIGHT)),
                  int(self.root.get(TiledLevel.TILEWIDTH)),
                  int(self.root.get(TiledLevel.TILEHEIGHT)))

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

            if obj.get(TiledLevel.NAME) == 'animations':
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
                                animated_tiles.update({''.join([animation_zindex, ' ', objx, ' ', objy]): animation_name})

        if not found:
            raise TiledLoaderError(_('Unable to find animations layer in level data.'))

        return animated_tiles

    def __load_tileset_info(self):
        tilesets = []

        for tileset in self.root.findall(TiledLevel.TILESET):
            tilewidth = int(tileset.get(TiledLevel.TILEWIDTH))
            tileheight = int(tileset.get(TiledLevel.TILEHEIGHT))
            firstgid = int(tileset.get(TiledLevel.FIRSTGID))
            name = tileset.get(TiledLevel.NAME)

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

                        if name == TiledLevel.START:
                            if prop.get(TiledLevel.VALUE) == 'True':
                                self.start_tile = tileid + firstgid

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

        return tiles

    def __load_layers_info(self):
        layers = []
        layerwidth = layerheight = layername = gid = None

        for layer in self.root.findall(TiledLevel.LAYER):
            layerwidth = int(layer.get(TiledLevel.WIDTH))
            layerheight = int(layer.get(TiledLevel.HEIGHT))
            layername = layer.get(TiledLevel.NAME)

            if layername in ['walls', 'background', 'special']:

                l = Layer(layername, (layerwidth, layerheight))

                for data in layer.findall(TiledLevel.DATA):
                    for tile in data.findall(TiledLevel.TILE):
                        gid = int(tile.get(TiledLevel.GID))

                        if gid in self.animated_tiles:
                            l.animated_tiles.append(gid)

                        l.data.append(gid)

                layers.append(l)

            else:
                pass
                #raise TiledLoaderError(_('Unknown layer %s found in level data.' % layername))
        return layers

    def __get_start_point(self):
        for l in self.layers:
            if l.name == TiledLevel.SPECIAL:
                for a in xrange(0, l.size[1]):
                    for i in xrange(0, l.size[0]):
                        if l.get_gid(i, a) == self.start_tile:
                            return i, a

    def __load(self, xml_data):
        self.root = ElementTree.fromstring(xml_data)

        # Read basic map info
        self.map = self.__load_map_info()

        # Read tileset info
        self.tilesets = self.__load_tileset_info()
        self.tiles = self.__load_tileset_graphics()

        # Read back info. Back info is the first image being rendered.
        self.back = self.__load_back_info()

        # Read animations info
        self.animated_tiles = self.__load_animations_info()

        # Read layers info
        self.layers = self.__load_layers_info()

        # Get starting point
        self.start_point = self.__get_start_point()

    def get_gid(self, x, y, name):
        for l in self.layers:
            if l.name == name:
                return l.get_gid(x, y)
        return 0

    def is_hard(self, x, y):
        if self.get_gid(x, y, TiledLevel.SPECIAL) in self.hard_tiles:
            return True

        return False
