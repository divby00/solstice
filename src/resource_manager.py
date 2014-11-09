import io
import pygame
import xml.etree.ElementTree as ElementTree
import zipfile
import i18n
import bitmap_font
import tiled_tools


class ResourceNotFoundError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class ResourceManager(object):

    def __init__(self, context, zipfilename, xmlfilename='resources.xml'):
        file_path = ''.join([context.cfg.data_path, zipfilename])
        self.zf = zipfile.ZipFile(file_path)
        xml = self.zf.read(xmlfilename)
        root = ElementTree.fromstring(xml)

        self.images_buffer = {}
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
            self.__update_load_screen(context.scr)

        self.__update_load_screen(context.scr)
        pygame.time.delay(500)

    def __update_load_screen(self, scr):
        scr.virt.fill((0, 0, 0, 0))

        if scr.icon:
            scr.virt.blit(scr.icon, (128-16, 55))

        bar_size = (self.actual_resource * 53) / self.total_resources
        pygame.draw.rect(scr.virt, (255, 255, 255), (102, 94, bar_size, 1), 1)
        pygame.draw.rect(scr.virt, (255, 255, 85), (102, 95, bar_size, 1), 1)
        pygame.draw.rect(scr.virt, (85, 255, 85), (102, 96, bar_size, 1), 1)
        pygame.draw.rect(scr.virt, (0, 170, 0), (102, 97, bar_size, 1), 1)

        '''
        for x in xrange(0, 52, 3):
            pygame.draw.rect(scr.virt, (0, 0, 0), (101+x, 93, 4, 6), 1)
        '''

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
            self.samples[name] = sample

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
            else:
                message = i18n._('Resource %s not found.' % res_name)
                raise ResourceNotFoundError(message)
        except ResourceNotFoundError as e:
            print(e.value)
