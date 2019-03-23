import io
import pygame
import xml.etree.cElementTree as ElementTree
import zipfile
from gettext import gettext as _

import animation
import bitmap_font
import tiled_tools


class ResourceNotFoundError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class ResourceManager(object):
    def __init__(self, context, zip_file_name, xml_file_name='resources.xml'):
        self._context = context
        self._zip_file = self._zip_file_open(zip_file_name)
        self._animation_loader = animation.AnimationLoader(self._zip_file)
        self._xml_root = self._read_resources_file(xml_file_name)
        self._images_cache = {}
        self._images = {}
        self._songs = {}
        self._samples = {}
        self._fonts = {}
        self._levels = {}
        self._animations = {}
        self._resources = self._xml_root.findall('resource')
        self._total_resources = len(self._xml_root.findall('resource'))
        self._actual_resource = 0

        for resource in self._xml_root.findall('resource'):
            if resource.get('type') == 'gfx':
                self._gfx_load(resource)
                self._actual_resource += 1
            elif resource.get('type') == 'music':
                if context.config.music:
                    self._load_song(resource)
                    self._actual_resource += 1
            elif resource.get('type') == 'sample':
                if context.config.sound:
                    self._load_sample(resource)
                    self._actual_resource += 1
            elif resource.get('type') == 'font':
                self._load_font(resource)
                self._actual_resource += 1
            elif resource.get('type') == 'level':
                self._load_level(resource)
                self._actual_resource += 1
            elif resource.get('type') == 'animation':
                self._load_animation(resource)
                self._actual_resource += 1
            self._update_load_screen(self._context.screen)

    '''
    Private methods
    '''

    def _zip_file_open(self, zip_file_name):
        file_path = ''.join([self._context.config.data_path, zip_file_name])
        return zipfile.ZipFile(file_path)

    def _read_resources_file(self, xml_file_name):
        xml = self._zip_file.read(xml_file_name)
        return ElementTree.fromstring(xml)

    def _update_load_screen(self, screen):
        screen.virtual_screen.fill((0, 0, 0, 0))
        if screen.icon:
            screen.virtual_screen.blit(screen.icon, (128 - 16, 55))

        bar_size = (self._actual_resource * 53) / self._total_resources
        pygame.draw.rect(screen.virtual_screen, (255, 255, 255), (102, 94, bar_size, 1), 1)
        pygame.draw.rect(screen.virtual_screen, (255, 255, 85), (102, 95, bar_size, 1), 1)
        pygame.draw.rect(screen.virtual_screen, (85, 255, 85), (102, 96, bar_size, 1), 1)
        pygame.draw.rect(screen.virtual_screen, (0, 170, 0), (102, 97, bar_size, 1), 1)
        pygame.transform.scale(screen.virtual_screen,
                               screen.scaling_resolution,
                               screen.scaled_virtual)
        screen.display.blit(screen.scaled_virtual, screen.final_offset)
        pygame.display.update()

    def _gfx_load(self, resource):
        src, name = ResourceManager.get_resource_common_info(resource)
        width = int(resource.get('width'))
        height = int(resource.get('height'))
        x = int(resource.get('x'))
        y = int(resource.get('y'))
        size = (width, height)
        position = (x, y)

        # Loading cache
        # Check if the image has been saved previously.
        if src in self._images_cache:
            temporary_surface = self._images_cache[src]
            self._surface_blit(name, size, position, temporary_surface)
        else:
            img_data = self._zip_file.read(src)
            byte_data = io.BytesIO(img_data)
            if byte_data is not None:
                temporary_surface = pygame.image.load(byte_data)
                self._surface_blit(name, size, position, temporary_surface)
                self._images_cache[src] = temporary_surface

    def _surface_blit(self, name, size, position, temporary_surface):
        surface = pygame.Surface(size)
        surface = surface.convert_alpha()
        surface.fill((0, 0, 0, 0))
        surface.blit(temporary_surface,
                     (0, 0),
                     (position[0], position[1], position[0] + size[0], position[1] + size[1]))
        self._images[name] = surface

    def _load_song(self, resource):
        src, name = ResourceManager.get_resource_common_info(resource)
        self._songs[name] = True

    def _load_song_reloading(self, song_name):
        song = None
        for resource in self._xml_root.findall('resource'):
            if resource.get('type') == 'music':
                src, name = ResourceManager.get_resource_common_info(resource)
                if name == song_name:
                    song_data = self._zip_file.read(src)
                    song = io.BytesIO(song_data)
        return song

    def _load_sample(self, resource):
        src, name = ResourceManager.get_resource_common_info(resource)
        sample_data = self._zip_file.read(src)
        sample = io.BytesIO(sample_data)
        if sample is not None:
            self._samples[name] = pygame.mixer.Sound(sample)

    def _load_font(self, resource):
        src, name = ResourceManager.get_resource_common_info(resource)
        rows = int(resource.get('rows'))
        columns = int(resource.get('columns'))
        fnt_data = self._zip_file.read(src)
        byte_data = io.BytesIO(fnt_data)
        if byte_data is not None:
            surface = pygame.image.load(byte_data)
            font = bitmap_font.BitmapFont(surface, rows, columns)
            if font is not None:
                self._fonts[name] = font

    def _load_level(self, resource):
        src, name = ResourceManager.get_resource_common_info(resource)
        lvl_data = self._zip_file.read(src)
        if lvl_data is not None:
            level = tiled_tools.TiledLevel(self._zip_file, lvl_data)
            if level is not None:
                self._levels[name] = level

    def _load_animation(self, resource):
        src, name = ResourceManager.get_resource_common_info(resource)
        animation_data = self._zip_file.read(src)
        if animation_data is not None:
            self._animations[name] = self._animation_loader.read(animation_data, name)

    '''
    Public methods
    '''

    @staticmethod
    def get_resource_common_info(resource):
        src = resource.get('src')
        name = resource.get('name')
        return src, name

    def exists(self, res_name):
        if res_name in self._images \
                or res_name in self._fonts \
                or res_name in self._samples \
                or res_name in self._levels:
            return True
        else:
            return False

    def get(self, resource_name):
        try:
            if resource_name in self._images:
                return self._images[resource_name]
            elif resource_name in self._songs:
                return self._load_song_reloading(resource_name)
            elif resource_name in self._fonts:
                return self._fonts[resource_name]
            elif resource_name in self._samples:
                return self._samples[resource_name]
            elif resource_name in self._levels:
                return self._levels[resource_name]
            elif resource_name in self._animations:
                return self._animations[resource_name]
            else:
                message = _('Resource %s not found.' % resource_name)
                raise ResourceNotFoundError(message)
        except ResourceNotFoundError as e:
            print(e.value)

    @property
    def animations(self):
        return self._animations
