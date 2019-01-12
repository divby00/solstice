import pygame


class ActiveInfoArea(object):
    def __init__(self, info_area_type, resource_manager):
        self._frame = -1
        self._active = True
        self._text = ActiveInfoArea._get_text_from_type(info_area_type)
        font_white = resource_manager.get('font_white')
        self._text_size = len(self._text) * font_white.glyph_width
        self._text_x = 256
        self._text_sprite = resource_manager.get('font_white').get(self._text, self._text_size)
        self._title_sprites = [resource_manager.get('info_area_title' + str(index))
                               for index in xrange(0, 9)]

    @staticmethod
    def _get_text_from_type(info_area_type):
        texts = dict(drill_wall='Use a drill to open the crate  ',
                     teleporter='Use a pass to use the teleporter  ')
        return texts[info_area_type]

    '''
    Public methods
    '''

    def run(self):
        self._frame += 1
        if self._frame >= 8:
            self._text_x -= 2
        return self._active

    def render(self, board):
        if self._active:
            pygame.draw.rect(board, (0, 0, 0), (0, 0, 256, 8), 0)
            if self._frame < 7:
                board.blit(self._title_sprites[self._frame], (0, 0))
            else:
                if self._text_x > self._text_size * -1:
                    board.blit(self._text_sprite, (self._text_x, 1))
                else:
                    board.blit(self._title_sprites[8], (0, 0))
                    self._active = False


class InfoArea(object):
    def __init__(self, position, size, info_area_type):
        self._position = position[0] + 256, position[1] + 144
        self._size = size
        self._info_area_type = info_area_type

    @property
    def position(self):
        return self._position

    @property
    def size(self):
        return self._size

    @property
    def info_area_type(self):
        return self._info_area_type


class InfoAreaBuilder(object):
    @staticmethod
    def build(info_areas):
        results = []
        for info_area in info_areas:
            info_area_elements = info_area.split(' ')
            x = int(info_area_elements[0])
            y = int(info_area_elements[1])
            w = int(info_area_elements[2])
            h = int(info_area_elements[3])
            info_area_type = info_area_elements[4]
            results.append(InfoArea((x, y), (w, h), info_area_type))

        return results
