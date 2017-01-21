class ActiveInfoArea(object):
    def __init__(self, info_area_type, resource_manager):
        self._frame = 0
        self._active = True
        self._text = ActiveInfoArea._get_text_from_type(info_area_type)
        self._text_sprite = resource_manager.get('font_board').get(self._text)
        self._title_sprites = [resource_manager.get('info_area_title' + str(index))
                               for index in xrange(0, 8)]

    @staticmethod
    def _get_text_from_type(info_area_type):
        texts = dict(drill_wall='You can open this block with a drill')
        return texts[info_area_type]

    '''
    Public methods
    '''

    def run(self):
        if self._active:
            if self._frame < 7:
                self._frame += 1
            else:
                self._active = False
                self._frame = 0

    def render(self, board):
        if self._active:
            board.blit(self._title_sprites[self._frame], (0, 0))


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
