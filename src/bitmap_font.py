import pygame


class BitmapFont(object):
    def __init__(self, surface, rows, columns):
        surface_width = surface.get_width()
        surface_height = surface.get_height()
        self._glyph_width = surface_width / columns
        self._glyph_height = surface_height / rows
        self._blank = pygame.Color(0, 0, 0, 0)
        self._glyph = []
        self._glyphs = {}

        for a in xrange(0, surface_height, self._glyph_height):

            for i in xrange(0, surface_width, self._glyph_width):
                dst_surface = pygame.Surface((self._glyph_width,
                                              self._glyph_height))

                if dst_surface is not None:
                    dst_surface = dst_surface.convert_alpha()
                    dst_surface.fill(self._blank)
                    dst_surface.blit(surface, (0, 0),
                                     (i, a, self._glyph_width, self._glyph_height), 0)
                    self._glyph.append(dst_surface)

    '''
    Private methods
    '''

    def _render(self, text, max_width):
        texts = []
        actual_text = 0
        texts.insert(0, '')
        output_text = ''

        for character in text.split():
            phrase_len = len(output_text) * self._glyph_width
            word_len = (len(character) + 1) * self._glyph_width

            if phrase_len + word_len < max_width:
                output_text += character + ' '
            else:
                texts.insert(actual_text, text.strip())
                actual_text += 1
                output_text = character + ' '

        texts.insert(actual_text, output_text.strip())
        texts.pop(len(texts) - 1)
        max_len = 0

        for character in texts:
            phrase_len = len(character) * self._glyph_width

            if phrase_len > max_len:
                max_len = phrase_len

        img_size = max_len, self._glyph_height * len(texts)
        dst_surface = pygame.Surface(img_size)

        if dst_surface is not None:
            dst_surface = dst_surface.convert_alpha()
            dst_surface.fill(self._blank)
            x = y = 0

            for character in texts:
                for c in character:
                    dst_surface.blit(self._glyph[ord(c)], (x, y))
                    x += self._glyph_width
                y += self._glyph_height
                x = 0

        self._glyphs[text] = dst_surface
        return dst_surface

    '''
    Public methods
    '''

    def get(self, text, max_width=None):
        if text in self._glyphs.keys():
            return self._glyphs[text]
        else:
            return self._render(text, max_width)

    @property
    def glyph_width(self):
        return self._glyph_width

    @property
    def glyph_height(self):
        return self._glyph_height
