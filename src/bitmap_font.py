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

    def get(self, text, max_width=None):
        assert(text is not None)
        assert(len(text) > 0)

        if text in self.glyphs.keys():
            return self.glyps[text]

        else:
            return self.__render(text, max_width)

    def __render(self, text, max_width):
        texts = []
        actual_text = 0
        texts.insert(0, '')
        texto = ''

        for t in text.split():
            phrase_len = len(texto) * self.gl_width
            word_len = (len(t) + 1) * self.gl_width

            if phrase_len + word_len < max_width:
                texto += t + ' '
            else:
                texts.insert(actual_text, texto.strip())
                actual_text += 1
                texto = t + ' '

        texts.insert(actual_text, texto.strip())
        texts.pop(len(texts)-1)
        max_len = 0

        for t in texts:
            phrase_len = len(t) * self.gl_width

            if phrase_len > max_len:
                max_len = phrase_len

        img_size = max_len, self.gl_height * len(texts)
        dst_surface = pygame.Surface(img_size)

        if dst_surface is not None:
            dst_surface = dst_surface.convert_alpha()
            dst_surface.fill(self.blank)
            x = y = 0

            for t in texts:
                for c in t:
                    dst_surface.blit(self.glyph[ord(c)], (x, y))
                    x += self.gl_width
                y += self.gl_height
                x = 0

        self.glyphs[text] = dst_surface
        return dst_surface
