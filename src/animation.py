import io
import pygame
import xml.etree.cElementTree as ElementTree


class Frame(object):
    pass


class Animation(object):

    def __init__(self, name):
        self.active_frame = 0
        self.counter = 0
        self.name = name
        self.images = {}
        self.frames = []


class AnimationLoader(object):
    
    def __init__(self, zip_file):
        self.zf = zip_file
        self.image_buffer = {}

    def read(self, xml_data, name):
        animation = Animation(name)
        root = ElementTree.fromstring(xml_data)

        for anim in root.findall('animation'):
            for images in anim.findall('images'):
                for image in images.findall('image'):
                    image_name = image.get('src')
                    image_id = int(image.get('id'))
                    image_x = int(image.get('x'))
                    image_y = int(image.get('y'))
                    image_w = int(image.get('width'))
                    image_h = int(image.get('height'))

                    if image_name not in self.image_buffer:
                        img_data = self.zf.read(image_name)
                        byte_data = io.BytesIO(img_data)

                        if byte_data is not None:
                            img = pygame.image.load(byte_data)

                            if img is not None:
                                srfc = pygame.Surface((image_w, image_h)).convert_alpha()
                                srfc.fill((0, 0, 0, 0))
                                srfc.blit(img, (0, 0), (image_x, image_y, image_x + image_w, image_y + image_h), 0)
                                self.image_buffer.update({image_name: img})
                                animation.images.update({str(image_id): srfc})
                    else:
                        img = self.image_buffer.get(image_name)

                        if img is not None:
                            srfc = pygame.Surface((image_w, image_h)).convert_alpha()
                            srfc.fill((0, 0, 0, 0))
                            srfc.blit(img, (0, 0), (image_x, image_y, image_x + image_w, image_y + image_h), 0)
                            animation.images.update({str(image_id): srfc})

            for frames in anim.findall('frames'):
                frame_order = 0

                for frame in frames.findall('frame'):
                    frame_id = int(frame.get('id'))
                    frame_offsetx = int(frame.get('offsetx'))
                    frame_offsety = int(frame.get('offsety'))
                    frame_duration = int(frame.get('duration'))
                    
                    fr = Frame()
                    fr.id = frame_id
                    fr.offsetx = frame_offsetx
                    fr.offsety = frame_offsety
                    fr.duration = frame_duration
                    animation.frames.insert(frame_order, fr)
                    frame_order += 1
        
        return animation
