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


class TiledLoader(object):

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

    def __init__(self, filename, tmxfile):
        self.zf = zipfile.ZipFile(filename)
        self.tiles = []
        self.layers = []
        self.__load(tmxfile)

    def __load(self, tmxfile):
        xml = self.zf.read(TiledLoader.LEVELS + tmxfile)
        imgwidth = 0
        imgheight = 0
        tilewidth = 0
        tileheight = 0
        firstgid = 0
        tilesets = []
        root = ElementTree.fromstring(xml)

        #Read basic map info
        self.map = Map(int(root.get(TiledLoader.WIDTH)), int(root.get(TiledLoader.HEIGHT)),
                       int(root.get(TiledLoader.TILEWIDTH)), int(root.get(TiledLoader.TILEHEIGHT)))

        #Read tileset info
        animated_tiles = []

        for tileset in root.findall(TiledLoader.TILESET):
            tilewidth = int(tileset.get(TiledLoader.TILEWIDTH))
            tileheight = int(tileset.get(TiledLoader.TILEHEIGHT))
            firstgid = int(tileset.get(TiledLoader.FIRSTGID))
            name = tileset.get(TiledLoader.NAME)

            for image in tileset.findall(TiledLoader.IMAGE):
                source = image.get(TiledLoader.SOURCE)
                imgwidth = int(image.get(TiledLoader.WIDTH))
                imgheight = int(image.get(TiledLoader.HEIGHT))

            for tile in tileset.findall(TiledLoader.TILE):
                tileid = int(tile.get(TiledLoader.ID))

                for properties in tile.findall(TiledLoader.PROPERTIES):
                    for property in properties:
                        name = property.get(TiledLoader.NAME)

                        if name == TiledLoader.ANIMATED:
                            if property.get(TiledLoader.VALUE) == 'True':
                                animated_tiles.append(tileid)

            tilesets.append(Tileset(name, imgwidth, imgheight, tilewidth,
                                    tileheight, source, firstgid))

        tilesets.sort(key=lambda obj: obj.firstgid)

        #Read background info
        source = None

        for imagelayer in root.findall(TiledLoader.IMAGELAYER):
            for image in imagelayer.findall(TiledLoader.IMAGE):
                source = image.get(TiledLoader.SOURCE)

        if source is not None:
            img_data = self.zf.read(TiledLoader.GFX + source)
            byte_data = io.BytesIO(img_data)

            if byte_data is not None:
                self.background = pygame.image.load(byte_data)

        #Read layer info
        layerwidth = layerheight = layername = gid = None

        for layer in root.findall(TiledLoader.LAYER):
            layerwidth = int(layer.get(TiledLoader.WIDTH))
            layerheight = int(layer.get(TiledLoader.HEIGHT))
            layername = layer.get(TiledLoader.NAME)
            l = Layer(layername, (layerwidth, layerheight))

            for properties in layer.findall(TiledLoader.PROPERTIES):
                for property in properties.findall(TiledLoader.PROPERTY):
                    prop = property.get(TiledLoader.NAME)

                    if prop == TiledLoader.ZINDEX:
                        l.zindex = int(property.get(TiledLoader.VALUE))

                    if prop == TiledLoader.VISIBLE:
                        l.visible = (property.get(TiledLoader.VALUE) == 'True')

            for data in layer.findall(TiledLoader.DATA):
                for tile in data.findall(TiledLoader.TILE):
                    gid = int(tile.get(TiledLoader.GID))

                    if gid in animated_tiles:
                        l.animated_tiles.append(gid)

                    l.data.append(gid)

            self.layers.append(l)

        self.layers.sort(key=lambda obj: obj.zindex)

        # Get beginning point
        for l in self.layers:

            if l.name == TiledLoader.SPECIAL:
                for a in xrange(0, l.size[1]):
                    for i in xrange(0, l.size[0]):

                        if l.get_gid(i, a) == 521:
                            self.start_point = (i, a)

        # Load tiles sprites
        img_count = 0
        blank = pygame.Color(0, 0, 0, 0)

        for t in tilesets:
            img_data = self.zf.read(TiledLoader.GFX + t.src)
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

        # TODO: Remove this
        img_data = self.zf.read(TiledLoader.GFX + 'marcador.png')
        byte_data = io.BytesIO(img_data)

        if byte_data is not None:
            self.marcador = pygame.image.load(byte_data)

        img_data = self.zf.read(TiledLoader.GFX + 'equinox.png')
        byte_data = io.BytesIO(img_data)

        if byte_data is not None:
            temp = pygame.image.load(byte_data)
            self.equinox = []
            self.animation = 0
            self.direction = 1

            for i in xrange(0, 1024/4, 64/4):
                srfc = pygame.Surface((64/4, 64/4))
                srfc = srfc.convert_alpha()
                srfc.fill(blank)
                srfc.blit(temp, (0, 0), (i, 0, i+(64/4), 64/4))
                self.equinox.append(srfc)

        img_data = self.zf.read(TiledLoader.GFX + 'tree.png')
        byte_data = io.BytesIO(img_data)

        if byte_data is not None:
            temp = pygame.image.load(byte_data)
            self.tree = []
            self.tanimation = 0

            for i in xrange(0, 1152/4, 192/4):
                srfc = pygame.Surface((192/4, 192/4))
                srfc = srfc.convert_alpha()
                srfc.fill(blank)
                srfc.blit(temp, (0, 0), (i, 0, i+(192/4), 192/4))
                self.tree.append(srfc)
        # Fin TODO

        self.zf.close()

    def get_gid(self, x, y, name):
        for l in self.layers:
            if l.name == name:
                return l.get_gid(x, y)
        return 0
