import pygame


class Pattern(object):
    def __init__(self, x, y, animation_name):
        self._x = x
        self._y = y
        self._animation_name = animation_name

    '''
    Public methods
    '''

    @property
    def animation_name(self):
        return self._animation_name

    @animation_name.setter
    def animation_name(self, value):
        self._animation_name = value

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Renderer(object):
    def __init__(self, context):
        self._font_white = context.font_white
        self._screen = context.screen
        self._level = context.current_level
        self._player = context.player
        self._enemies = context.enemies
        self._items = context.items
        self._animations = context.animations
        self._particles_manager = context.particles_manager
        self._player = context.player
        self._board = context.board
        self._speed = 4, 4
        self._start_point = self._get_start_point()
        self._source, self._fore_source = self._init_source_image()
        self._backpatterns = []
        self._forepatterns = []
        self._init_patterns()
        self._tmp_surface = pygame.Surface((self._source.get_width(), self._source.get_height()))\
            .convert()
        self._tmp_surface.fill((0, 0, 0, 0))

    '''
    Private methods
    '''

    def _init_patterns(self):
        animations = self._level.animated_tiles
        for animation in animations:
            data = animation.split(' ')
            zindex = data[0]
            animation_x = data[1]
            animation_y = data[2]
            animation_name = animations.get(animation)
            pattern = Pattern(int(animation_x) + 256, int(animation_y) + 144, animation_name)
            if zindex == '0':
                self._backpatterns.append(pattern)
            else:
                self._forepatterns.append(pattern)

    def _get_start_point(self):
        return ((self._level.start_point[0]) + 256 + 8) - 128, \
               ((self._level.start_point[1]) + 144 + 8) - 72

    def _init_source_image(self):
        back_tiles_overflow = []
        fore_tiles_overflow = []
        level_size = self._level.map.width_pixels, self._level.map.height_pixels
        back = pygame.Surface((level_size[0] + 512, level_size[1] + 288)).convert()
        back.fill((0, 0, 0))
        fore = pygame.Surface((level_size[0] + 512, level_size[1] + 288)).convert_alpha()
        fore.fill((0, 0, 0, 0))
        back_img = self._level.back
        walls = pygame.Surface(level_size).convert_alpha()
        walls.fill((0, 0, 0, 0))

        # Draw the back image in the buffer
        for a in xrange(0, back.get_height(), back_img.get_height()):
            for i in xrange(0, back.get_width(), back_img.get_width()):
                back.blit(back_img, (i, a))

        # Draw the background in the buffer
        for layer in self._level.layers:
            if layer.name == 'background':
                posx = posy = 0
                for a in xrange(0, level_size[1] / 8):
                    for i in xrange(0, level_size[0] / 8):
                        gid = layer.get_gid(i, a)
                        if gid > 0 and gid < len(self._level.tiles):
                            walls.blit(self._level.tiles[gid - 1].srfc, (posx, posy))
                        else:
                            if gid > 0:
                                back_tiles_overflow.append(gid)
                        posx += 8
                    posx = 0
                    posy += 8

        # Draw the walls in the buffer
        for layer in self._level.layers:
            if layer.name == 'walls':
                posx = posy = 0
                for a in xrange(0, level_size[1] / 8):
                    for i in xrange(0, level_size[0] / 8):
                        gid = layer.get_gid(i, a)
                        if gid > 0 and gid < len(self._level.tiles):
                            walls.blit(self._level.tiles[gid - 1].srfc, (posx, posy))
                        else:
                            if gid > 0:
                                fore_tiles_overflow.append(gid)
                        posx += 8
                    posx = 0
                    posy += 8

        # Draws hard zones.
        # TODO Remove this. Only for debugging purpose!!
        '''
        for l in self.level.layers:
            if l.name == 'hard':
                posx = posy = 0
                for a in xrange(0, level_size[1] / 8):
                    for i in xrange(0, level_size[0] / 8):
                        gid = l.get_gid(i, a)
                        if gid in self.level.hard_tiles:
                            walls.blit(self.level.tiles[518].srfc, (posx, posy))
                        posx += 8
                    posx = 0
                    posy += 8
        '''
        # End debugging walls

        # Draw the foreground static images in the fore buffer
        for layer in self._level.layers:
            if layer.name == 'foreground':
                posx = posy = 0
                for a in xrange(0, level_size[1] / 8):
                    for i in xrange(0, level_size[0] / 8):
                        gid = layer.get_gid(i, a)
                        if gid > 0 and gid < len(self._level.tiles):
                            fore.blit(self._level.tiles[gid - 1].srfc, (posx, posy))
                        else:
                            if gid > 0:
                                fore_tiles_overflow.append(gid)
                        posx += 8
                    posx = 0
                    posy += 8

        x = (back.get_width() / 2) - (walls.get_width() / 2)
        y = (back.get_height() / 2) - (walls.get_height() / 2)
        back.blit(walls, (x, y))
        '''
        # Debugging purposes
        print(set(back_tiles_overflow))
        print(set(fore_tiles_overflow))
        '''
        return back, fore

    '''
    Public methods
    '''

    def change_animation(self, position, new_anim):
        for backpattern in self._backpatterns:
            if backpattern.x == position[0] and backpattern.y == position[1]:
                if new_anim is None:
                    self._backpatterns.remove(backpattern)
                else:
                    backpattern.animation_name = new_anim

        for backpattern in self._forepatterns:
            if backpattern.x == position[0] and backpattern.y == position[1]:
                if new_anim is None:
                    self._forepatterns.remove(backpattern)
                else:
                    backpattern.animation_name = new_anim

    def run(self):
        for pattern in self._backpatterns:
            anim = self._animations.get(pattern.animation_name)

            if anim.counter < anim.frames[anim.active_frame].duration:
                anim.counter += 1
            else:
                anim.counter = 0

                if anim.active_frame < len(anim.frames) - 1:
                    anim.active_frame += 1
                else:
                    anim.active_frame = 0

        for pattern in self._forepatterns:
            anim = self._animations.get(pattern.animation_name)

            if anim.counter < anim.frames[anim.active_frame].duration:
                anim.counter += 1
            else:
                anim.counter = 0

                if anim.active_frame < len(anim.frames) - 1:
                    anim.active_frame += 1
                else:
                    anim.active_frame = 0

    def render(self):
        # Source rendering
        self._tmp_surface.blit(self._source,
                               (self._player.x - 128, self._player.y - 72),
                               (self._player.x - 128, self._player.y - 72, 256, 144))

        # Backpattern rendering
        for pattern in self._backpatterns:
            animation = self._animations.get(pattern.animation_name)
            img = animation.images.get(str(animation.frames[animation.active_frame].id))
            self._tmp_surface.blit(img, (pattern.x + animation.frames[animation.active_frame].offset_x, pattern.y + animation.frames[animation.active_frame].offset_y))

        # Player rendering
        self._player.render(self._tmp_surface)

        # Enemies rendering
        for enemy in self._enemies:
            enemy.render(self._tmp_surface)

        # Particles rendering
        self._particles_manager.render(self._tmp_surface)

        # Foreground Source rendering
        self._tmp_surface.blit(self._fore_source,
                               (self._player.x - 128, self._player.y - 72),
                               (self._player.x - 384, self._player.y - 216, 256, 144))

        # Forepattern rendering
        for pattern in self._forepatterns:
            animation = self._animations.get(pattern.animation_name)
            img = animation.images.get(str(animation.frames[animation.active_frame].id))
            self._tmp_surface.blit(img,
                                   (pattern.x + animation.frames[animation.active_frame].offset_x, pattern.y + animation.frames[animation.active_frame].offset_y))

        # Viewport rendering
        self._screen.virt.blit(self._tmp_surface, (0, 0), (self._player.x - 128, self._player.y - 72, 256, 144))

        # Board rendering
        self._board.render(self._screen.virt)

        # Debug information
        '''
        pygame.draw.rect(self.screen.virt, (30, 30, 30), (0, 0, 100, 20), 0)
        text = self.font_white.get(('x:' + str(self.player.x - 264) + ' y:' + str(self.player.y - 152)), 100)
        self.screen.virt.blit(text, (5, 5))
        '''

    @property
    def speed(self):
        return self._speed
