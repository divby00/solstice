import io
import pygame
import xml.etree.ElementTree as ElementTree
from gettext import gettext as _
import zipfile

import bitmap_font
import tiled_tools
import animation


class ResourceNotFoundError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class ResourceManager(object):
    def __init__(self, context, zipfilename, xmlfilename='resources.xml'):
        file_path = ''.join([context.cfg.data_path, zipfilename])
        self.zf = zipfile.ZipFile(file_path)
        self.anim_loader = animation.AnimationLoader(self.zf)
        xml = self.zf.read(xmlfilename)
        root = ElementTree.fromstring(xml)

        self.images_buffer = {}
        self.images = {}
        self.songs = {}
        self.samples = {}
        self.fonts = {}
        self.levels = {}
        self.animations = {}
        self.resources = root.findall('resource')
        self.total_resources = len(root.findall('resource'))
        self.actual_resource = 0

        for resource in root.findall('resource'):
            before = pygame.time.get_ticks()
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
            elif resource.get('type') == 'animation':
                self.__load_animation(resource)
                self.actual_resource += 1
            after = pygame.time.get_ticks()
            print('Resource %s loaded in %d milliseconds.' % (resource.get('name'), (after - before)))
            self.__update_load_screen(context.scr)


        self.__update_load_screen(context.scr)
        pygame.time.delay(200)

    def __update_load_screen(self, scr):
        scr.virt.fill((0, 0, 0, 0))

        if scr.icon:
            scr.virt.blit(scr.icon, (128 - 16, 55))

        bar_size = (self.actual_resource * 53) / self.total_resources
        pygame.draw.rect(scr.virt, (255, 255, 255), (102, 94, bar_size, 1), 1)
        pygame.draw.rect(scr.virt, (255, 255, 85), (102, 95, bar_size, 1), 1)
        pygame.draw.rect(scr.virt, (85, 255, 85), (102, 96, bar_size, 1), 1)
        pygame.draw.rect(scr.virt, (0, 170, 0), (102, 97, bar_size, 1), 1)
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

        # Load optimization
        # Check if the image has been saved previously.
        if src in self.images_buffer:
            temp = self.images_buffer[src]
            srfc = pygame.Surface((width, height))
            srfc = srfc.convert_alpha()
            srfc.fill((0, 0, 0, 0))
            srfc.blit(temp, (0, 0), (x, y, x + width, y + height))
            self.images[name] = srfc
        else:
            img_data = self.zf.read(src)
            byte_data = io.BytesIO(img_data)

            if byte_data is not None:
                temp = pygame.image.load(byte_data)
                srfc = pygame.Surface((width, height))
                srfc = srfc.convert_alpha()
                srfc.fill((0, 0, 0, 0))
                srfc.blit(temp, (0, 0), (x, y, x + width, y + height))
                self.images[name] = srfc
                self.images_buffer[src] = temp

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
            self.samples[name] = pygame.mixer.Sound(sample)

    def __load_font(self, resource):
        src, name = self.__get_common_info(resource)
        rows = int(resource.get('rows'))
        columns = int(resource.get('columns'))
        fnt_data = self.zf.read(src)
        byte_data = io.BytesIO(fnt_data)

        if byte_data is not None:
            surface = pygame.image.load(byte_data)
            font = bitmap_font.BitmapFont(surface, rows, columns)

            if font is not None:
                self.fonts[name] = font

    def __load_level(self, resource):
        src, name = self.__get_common_info(resource)
        before = pygame.time.get_ticks()
        lvl_data = self.zf.read(src)
        after = pygame.time.get_ticks()
        print('\tLEVEL: File read in %d milliseconds.' % (after - before))

        if lvl_data is not None:
            level = tiled_tools.TiledLevel(self.zf, lvl_data)

            if level is not None:
                self.levels[name] = level

    def __load_animation(self, resource):
        src, name = self.__get_common_info(resource)
        anim_data = self.zf.read(src)

        if anim_data is not None:
            self.animations[name] = self.anim_loader.read(anim_data, name)

    @staticmethod
    def __get_common_info(resource):
        src = resource.get('src')
        name = resource.get('name')
        return src, name

    def exists(self, res_name):
        if res_name in self.images or \
                        res_name in self.songs or \
                        res_name in self.fonts or \
                        res_name in self.samples or \
                        res_name in self.levels:
            return True
        else:
            return False

    def get(self, res_name):
        try:
            if res_name in self.images:
                return self.images[res_name]
            elif res_name in self.songs:
                return self.songs[res_name]
            elif res_name in self.fonts:
                return self.fonts[res_name]
            elif res_name in self.samples:
                return self.samples[res_name]
            elif res_name in self.levels:
                return self.levels[res_name]
            elif res_name in self.animations:
                return self.animations[res_name]
            else:
                message = _('Resource %s not found.' % res_name)
                raise ResourceNotFoundError(message)
        except ResourceNotFoundError as e:
            print(e.value)
