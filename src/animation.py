import io
import pygame
import xml.etree.cElementTree as ElementTree


class Frame(object):
    def __init__(self):
        self._id = None
        self._offset_x = 0
        self._offset_y = 0
        self._duration = 0

    '''
    Public methods
    '''

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def offset_x(self):
        return self._offset_x

    @offset_x.setter
    def offset_x(self, value):
        self._offset_x = value

    @property
    def offset_y(self):
        return self._offset_y

    @offset_y.setter
    def offset_y(self, value):
        self._offset_y = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value


class Animation(object):
    def __init__(self, name):
        self._active_frame = 0
        self._counter = 0
        self._name = name
        self._images = {}
        self._frames = []

    '''
    Public methods
    '''

    @property
    def frames(self):
        return self._frames

    @property
    def images(self):
        return self._images

    @property
    def active_frame(self):
        return self._active_frame

    @active_frame.setter
    def active_frame(self, value):
        self._active_frame = value

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, value):
        self._counter = value


class AnimationLoader(object):
    def __init__(self, zip_file):
        self._zip_file = zip_file
        self._image_buffer = {}

    '''
    Public methods
    '''

    def read(self, animation_data, name):
        animation = Animation(name)
        root = ElementTree.fromstring(animation_data)

        for anim in root.findall('animation'):
            for images in anim.findall('images'):
                for image in images.findall('image'):
                    image_name = image.get('src')
                    image_id = int(image.get('id'))
                    image_x = int(image.get('x'))
                    image_y = int(image.get('y'))
                    image_w = int(image.get('width'))
                    image_h = int(image.get('height'))

                    if image_name not in self._image_buffer:
                        img_data = self._zip_file.read(image_name)
                        byte_data = io.BytesIO(img_data)

                        if byte_data is not None:
                            img = pygame.image.load(byte_data)

                            if img is not None:
                                surface = pygame.Surface((image_w, image_h)).convert_alpha()
                                surface.fill((0, 0, 0, 0))
                                surface.blit(img, (0, 0),
                                             (image_x, image_y, image_x + image_w,
                                              image_y + image_h), 0)
                                self._image_buffer.update({image_name: img})
                                animation.images.update({str(image_id): surface})
                    else:
                        img = self._image_buffer.get(image_name)

                        if img is not None:
                            surface = pygame.Surface((image_w, image_h)).convert_alpha()
                            surface.fill((0, 0, 0, 0))
                            surface.blit(img, (0, 0),
                                         (image_x, image_y, image_x + image_w, image_y + image_h),
                                         0)
                            animation.images.update({str(image_id): surface})

            for frames in anim.findall('frames'):
                frame_order = 0

                for frame in frames.findall('frame'):
                    frame_id = int(frame.get('id'))
                    frame_offset_x = int(frame.get('offsetx'))
                    frame_offset_y = int(frame.get('offsety'))
                    frame_duration = int(frame.get('duration'))

                    fr = Frame()
                    fr.id = frame_id
                    fr.offset_x = frame_offset_x
                    fr.offset_y = frame_offset_y
                    fr.duration = frame_duration
                    animation.frames.insert(frame_order, fr)
                    frame_order += 1

        return animation
