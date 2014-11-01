import pygame
import io
import xml.etree.ElementTree as ElementTree
import zipfile
import bitmapfont
import tiled_tools


class ResourceManager(object):

    def __init__(self, zipfilename, xmlfilename='resources.xml'):
        self.zf = zipfile.ZipFile(zipfilename)
        xml = self.zf.read(xmlfilename)
        root = ElementTree.fromstring(xml)

        self.images = {}
        self.songs = {}
        self.samples = {}
        self.fonts = {}
        self.levels = {}
        self.resources = root.findall('resource')

        for resource in root.findall('resource'):
            if resource.get('type')=='gfx':
                self.load_gfx(resource)
            elif resource.get('type')=='music':
                self.load_song(resource)
            elif resource.get('type')=='sample':
                self.load_sample(resource)
            elif resource.get('type')=='font':
                self.load_font(resource)
            elif resource.get('type')=='level':
                self.load_level(resource)

        print('Loaded %d images' % len(self.images))
        print('Loaded %d songs' % len(self.songs))
        print('Loaded %d fonts' % len(self.fonts))
        print('Loaded %d levels' % len(self.levels))

    def load_gfx(self, resource):
        src = resource.get('src')
        width = int(resource.get('width'))
        height = int(resource.get('height'))
        x = int(resource.get('x'))
        y = int(resource.get('y'))
        name = resource.get('name')
        img_data = self.zf.read(src)
        byte_data = io.BytesIO(img_data)

        if byte_data is not None:
            temp = pygame.image.load(byte_data)
            srfc = pygame.Surface((width, height))
            srfc = srfc.convert_alpha()
            srfc.fill((0, 0, 0, 0))
            srfc.blit(temp, (0, 0), (x, y, x + width, y + height))
            self.images[name] = srfc

    def load_song(self, resource):
        src = resource.get('src')
        name = resource.get('name')
        song_data = self.zf.read(src)
        song = io.BytesIO(song_data)

        if song is not None:
            self.songs[name] = song

    def load_sample(self, resource):
        src = resource.get('src')
        name = resource.get('name')
        sample_data = self.zf.read(src)
        sample = io.BytesIO(sample_data)

        if sample is not None:
            self.samples[name] = sample

    def load_font(self, resource):
        src = resource.get('src')
        name = resource.get('name')
        rows = int(resource.get('rows'))
        columns = int(resource.get('columns'))
        fnt_data = self.zf.read(src)
        byte_data = io.BytesIO(fnt_data)

        if byte_data is not None:
            surface = pygame.image.load(byte_data)
            font = bitmapfont.BitmapFont(surface, rows, columns)

            if font is not None:
                self.fonts[name] = font

    def load_level(self, resource):
        src = resource.get('src')
        name = resource.get('name')
        lvl_data = self.zf.read(src)

        if lvl_data is not None:
            level = tiled_tools.TiledLevel(self.zf, lvl_data)

            if level is not None:
                self.levels[name] = level

    def get(self, res_name):
        if self.images.has_key(res_name):
            return self.images[res_name]
        elif self.songs.has_key(res_name):
            return self.songs[res_name]
        elif self.fonts.has_key(res_name):
            return self.fonts[res_name]
        elif self.samples.has_key(res_name):
            return self.samples[res_name]
        elif self.levels.has_key(res_name):
            return self.levels[res_name]

