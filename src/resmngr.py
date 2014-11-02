import pygame
import io
import xml.etree.ElementTree as ElementTree
import zipfile
import bitmapfont
import tiled_tools


class ResourceManager(object):

    def __init__(self, scr, cfg, zipfilename, xmlfilename='resources.xml'):
        file_path = ''.join([cfg.data_path, zipfilename])
        self.zf = zipfile.ZipFile(file_path)
        xml = self.zf.read(xmlfilename)
        root = ElementTree.fromstring(xml)

        self.images = {}
        self.songs = {}
        self.samples = {}
        self.fonts = {}
        self.levels = {}
        self.resources = root.findall('resource')
        self.total_resources = len(root.findall('resource'))
        self.actual_resource = 0

        for resource in root.findall('resource'):
            if resource.get('type') == 'gfx':
                self.__load_gfx(resource)
                self.actual_resource += 1
            elif resource.get('type') == 'music':
                self.__load_song(resource)
                self.actual_resource += 1
            elif resource.get('type') == 'sample':
                self.__load_sample(resource)
                self.actual_resource += 1
            elif resource.get('type') == 'font':
                self.__load_font(resource)
                self.actual_resource += 1
            elif resource.get('type') == 'level':
                self.__load_level(resource)
                self.actual_resource += 1
            self.__update_load_screen(scr)

        self.__update_load_screen(scr)
        pygame.time.delay(500)

    def __update_load_screen(self, scr):
        scr.virt.fill((0, 0, 0, 0))
        pygame.draw.rect(scr.virt, (0, 170, 0), (100, 92, 56, 8), 1)
        bar_size = (self.actual_resource * 52) / self.total_resources
        pygame.draw.rect(scr.virt, (85, 255, 85), (102, 94, bar_size, 4), 0)
        pygame.transform.scale(scr.virt,
                               scr.screen_size,
                               scr.display)
        pygame.display.update()

    def __load_gfx(self, resource):
        src, name = self.__get_common_info(resource)
        width = int(resource.get('width'))
        height = int(resource.get('height'))
        x = int(resource.get('x'))
        y = int(resource.get('y'))
        img_data = self.zf.read(src)
        byte_data = io.BytesIO(img_data)

        if byte_data is not None:
            temp = pygame.image.load(byte_data)
            srfc = pygame.Surface((width, height))
            srfc = srfc.convert_alpha()
            srfc.fill((0, 0, 0, 0))
            srfc.blit(temp, (0, 0), (x, y, x + width, y + height))
            self.images[name] = srfc

    def __load_song(self, resource):
        src, name = self.__get_common_info(resource)
        song_data = self.zf.read(src)
        song = io.BytesIO(song_data)

        if song is not None:
            self.songs[name] = song

    def __load_sample(self, resource):
        src, name = self.__get_common_info(resource)
        sample_data = self.zf.read(src)
        sample = io.BytesIO(sample_data)

        if sample is not None:
            self.samples[name] = sample

    def __load_font(self, resource):
        src, name = self.__get_common_info(resource)
        rows = int(resource.get('rows'))
        columns = int(resource.get('columns'))
        fnt_data = self.zf.read(src)
        byte_data = io.BytesIO(fnt_data)

        if byte_data is not None:
            surface = pygame.image.load(byte_data)
            font = bitmapfont.BitmapFont(surface, rows, columns)

            if font is not None:
                self.fonts[name] = font

    def __load_level(self, resource):
        src, name = self.__get_common_info(resource)
        lvl_data = self.zf.read(src)

        if lvl_data is not None:
            level = tiled_tools.TiledLevel(self.zf, lvl_data)

            if level is not None:
                self.levels[name] = level

    def __get_common_info(self, resource):
        src = resource.get('src')
        name = resource.get('name')
        return src, name

    def get(self, res_name):
        if self.images in res_name:
            return self.images[res_name]
        elif self.songs in res_name:
            return self.songs[res_name]
        elif self.fonts in res_name:
            return self.fonts[res_name]
        elif self.samples in res_name:
            return self.samples[res_name]
        elif self.levels in res_name:
            return self.levels[res_name]
