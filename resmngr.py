import pygame
import io
import zipfile
import bitmapfont
import xml.etree.ElementTree as ElementTree


class ResourceManager(object):

    def __init__(self, zipfilename, xmlfilename='resources.xml'):
        self.zf = zipfile.ZipFile(zipfilename)
        xml = self.zf.read(xmlfilename)
        root = ElementTree.fromstring(xml)

        self.images = {}
        self.songs = {}
        self.fonts = {}

        for resource in root.findall('resource'):
            if resource.get('type')=='gfx':
                self.load_gfx(resource)
            elif resource.get('type')=='music':
                self.load_song(resource)
            elif resource.get('type')=='font':
                self.load_font(resource)

        '''
        print('Loaded %d images' % len(self.images))
        print('Loaded %d songs' % len(self.songs))
        print('Loaded %d fonts' % len(self.fonts))
        '''

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

    def get(self, res_name):
        if self.images.has_key(res_name):
            return self.images[res_name]
        elif self.songs.has_key(res_name):
            return self.songs[res_name]
        elif self.fonts.has_key(res_name):
            return self.fonts[res_name]

