import pygame
import io
import zipfile
import xml.etree.ElementTree as ElementTree


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
        self.zindex = None
        self.visible = False
        self.animated_tiles = []

    def get_gid(self, x, y):

        if x < 0 or y < 0:
            return 0

        if (y * self.size[0]) + x >= (self.size[0] * self.size[1]):
            return 0

        return self.data[(y * self.size[0]) + x]

    def __cmp__(self, other):
        return cmp(self.zindex, other.zindex)


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
    PROPERTY = 'property'
    SPECIAL = 'special'
    VISIBLE = 'visible'
    ZINDEX = 'zindex'
    GID = 'gid'
    DATA = 'data'
    VALUE = 'value'
    LAYER = 'layer'
    IMAGE = 'image'
    SOURCE = 'source'
    ANIMATED = 'animated'
    ID = 'id'
    IMAGELAYER = 'imagelayer'
    FIRSTGID = 'firstgid'

    def __init__(self, zf, xml_data):
        self.tiles = []
        self.layers = []
        self.zf = zf
        self.__load(xml_data)

    def __load(self, xml_data):
        imgwidth = 0
        imgheight = 0
        tilewidth = 0
        tileheight = 0
        firstgid = 0
        tilesets = []
        root = ElementTree.fromstring(xml_data)

        #Read basic map info
        self.map = Map(int(root.get(TiledLevel.WIDTH)), int(root.get(TiledLevel.HEIGHT)),
                       int(root.get(TiledLevel.TILEWIDTH)), int(root.get(TiledLevel.TILEHEIGHT)))

        #Read tileset info
        animated_tiles = []

        for tileset in root.findall(TiledLevel.TILESET):
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
                    for property in properties:
                        name = property.get(TiledLevel.NAME)

                        if name == TiledLevel.ANIMATED:
                            if property.get(TiledLevel.VALUE) == 'True':
                                animated_tiles.append(tileid)

            tilesets.append(Tileset(name, imgwidth, imgheight, tilewidth,
                                    tileheight, source, firstgid))

        tilesets.sort(key=lambda obj: obj.firstgid)

        #Read background info
        source = None

        for imagelayer in root.findall(TiledLevel.IMAGELAYER):
            for image in imagelayer.findall(TiledLevel.IMAGE):
                source = image.get(TiledLevel.SOURCE)

        if source is not None:
            img_data = self.zf.read(TiledLevel.GFX + source)
            byte_data = io.BytesIO(img_data)

            if byte_data is not None:
                self.background = pygame.image.load(byte_data)

        #Read layer info
        layerwidth = layerheight = layername = gid = None

        for layer in root.findall(TiledLevel.LAYER):
            layerwidth = int(layer.get(TiledLevel.WIDTH))
            layerheight = int(layer.get(TiledLevel.HEIGHT))
            layername = layer.get(TiledLevel.NAME)
            l = Layer(layername, (layerwidth, layerheight))

            for properties in layer.findall(TiledLevel.PROPERTIES):
                for property in properties.findall(TiledLevel.PROPERTY):
                    prop = property.get(TiledLevel.NAME)

                    if prop == TiledLevel.ZINDEX:
                        l.zindex = int(property.get(TiledLevel.VALUE))

                    if prop == TiledLevel.VISIBLE:
                        l.visible = (property.get(TiledLevel.VALUE) == 'True')

            for data in layer.findall(TiledLevel.DATA):
                for tile in data.findall(TiledLevel.TILE):
                    gid = int(tile.get(TiledLevel.GID))

                    if gid in animated_tiles:
                        l.animated_tiles.append(gid)

                    l.data.append(gid)

            self.layers.append(l)

        self.layers.sort(key=lambda obj: obj.zindex)

        # Get beginning point
        for l in self.layers:

            if l.name == TiledLevel.SPECIAL:
                for a in xrange(0, l.size[1]):
                    for i in xrange(0, l.size[0]):

                        if l.get_gid(i, a) == 521:
                            self.start_point = (i, a)

        # Load tiles sprites
        img_count = 0
        blank = pygame.Color(0, 0, 0, 0)

        for t in tilesets:
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

                        self.tiles.append(Tile(srfc, (t.tilew, t.tileh)))
                        img_count += 1

    def get_gid(self, x, y, name):
        for l in self.layers:
            if l.name == name:
                return l.get_gid(x, y)
        return 0
