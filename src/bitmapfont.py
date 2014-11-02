import pygame
import zipfile
import io


class BitmapFont(object):


    def __init__(self, surface, rows, columns):

        w = surface.get_width()
        h = surface.get_height()

        assert(w > 0)
        assert(h > 0)

        self.gl_width = w / columns
        self.gl_height = h / rows
        self.blank = pygame.Color(0, 0, 0, 0)
        self.glyph = []
        self.glyphs = {}

        for a in xrange(0, h, self.gl_height):

            for i in xrange(0, w, self.gl_width):
                dst_surface = pygame.Surface((self.gl_width,
                                              self.gl_height))

                if dst_surface is not None:
                    dst_surface = dst_surface.convert_alpha()
                    dst_surface.fill(self.blank)
                    dst_surface.blit(surface, (0, 0),
                                    (i, a, self.gl_width, self.gl_height), 0)
                    self.glyph.append(dst_surface)

    def get(self, text):
        assert(text is not None)
        assert(len(text) > 0)

        if text in self.glyphs.keys():
            return self.glyps[text]

        else:
            return self.__render(text)

    def __render(self, text):
        img_size = (len(text) * self.gl_width, self.gl_height)
        dst_surface = pygame.Surface(img_size)

        if dst_surface is not None:
            dst_surface = dst_surface.convert_alpha()
            dst_surface.fill(self.blank)
            x = y = 0

            for c in text:
                dst_surface.blit(self.glyph[ord(c)], (x, y))
                x += self.gl_width

        self.glyphs[text] = dst_surface
        return dst_surface
