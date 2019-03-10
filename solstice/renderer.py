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
        self._crushers = context.crushers
        self._powerups = context.powerups
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
        self._tmp_surface = pygame.Surface((self._source.get_width(), self._source.get_height())) \
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
            if zindex == '0' and animation_name != 'object017':
                self._backpatterns.append(pattern)
            else:
                self._forepatterns.append(pattern)

    def _get_start_point(self):
        return ((self._level.start_point[0]) + 256 + 8) - 128, \
               ((self._level.start_point[1]) + 144 + 8) - 72

    def _init_source_image(self):
        level_size = self._level.map.width_pixels, self._level.map.height_pixels
        back_dst_surface = pygame.Surface((level_size[0] + 512, level_size[1] + 288)).convert()
        back_dst_surface.fill((0, 0, 0))
        fore_dst_surface = pygame.Surface(
            (level_size[0] + 512, level_size[1] + 288)).convert_alpha()
        fore_dst_surface.fill((0, 0, 0, 0))
        walls_dst_surface = pygame.Surface(level_size).convert_alpha()
        walls_dst_surface.fill((0, 0, 0, 0))

        # Draw images in the buffer
        self._draw_back_image(back_dst_surface)
        self._draw_background_image(walls_dst_surface, level_size)
        self._draw_walls_image(walls_dst_surface, level_size)
        self._draw_foreground_image(fore_dst_surface, level_size)

        x = (back_dst_surface.get_width() / 2) - (walls_dst_surface.get_width() / 2)
        y = (back_dst_surface.get_height() / 2) - (walls_dst_surface.get_height() / 2)
        back_dst_surface.blit(walls_dst_surface, (x, y))
        return back_dst_surface, fore_dst_surface

    def _draw_back_image(self, back_dst_surface):
        for a in xrange(0, back_dst_surface.get_height(), self._level.back.get_height()):
            for i in xrange(0, back_dst_surface.get_width(), self._level.back.get_width()):
                back_dst_surface.blit(self._level.back, (i, a))

    def _draw_background_image(self, walls_dst_surface, level_size):
        for layer in self._level.layers:
            if layer.name == 'background':
                posx = posy = 0
                for a in xrange(0, level_size[1] / 8):
                    for i in xrange(0, level_size[0] / 8):
                        gid = layer.get_gid(i, a)
                        if 0 < gid < len(self._level.tiles):
                            walls_dst_surface.blit(self._level.tiles[gid - 1].srfc, (posx, posy))
                        posx += 8
                    posx = 0
                    posy += 8

    def _draw_walls_image(self, walls_dst_surface, level_size):
        for layer in self._level.layers:
            if layer.name == 'walls':
                posx = posy = 0
                for a in xrange(0, level_size[1] / 8):
                    for i in xrange(0, level_size[0] / 8):
                        gid = layer.get_gid(i, a)
                        if 0 < gid < len(self._level.tiles):
                            walls_dst_surface.blit(self._level.tiles[gid - 1].srfc, (posx, posy))
                        posx += 8
                    posx = 0
                    posy += 8

    def _draw_foreground_image(self, fore_dst_surface, level_size):
        for layer in self._level.layers:
            if layer.name == 'foreground':
                posx = posy = 0
                for a in xrange(0, level_size[1] / 8):
                    for i in xrange(0, level_size[0] / 8):
                        gid = layer.get_gid(i, a)
                        if 0 < gid < len(self._level.tiles):
                            fore_dst_surface.blit(self._level.tiles[gid - 1].srfc, (posx, posy))
                        posx += 8
                    posx = 0
                    posy += 8

    def _run_animation(self, patterns):
        for pattern in patterns:
            animation = self._animations.get(pattern.animation_name)

            if animation.counter < animation.frames[animation.active_frame].duration:
                animation.counter += 1
            else:
                animation.counter = 0

                if animation.active_frame < len(animation.frames) - 1:
                    animation.active_frame += 1
                else:
                    animation.active_frame = 0

    '''
    Public methods
    '''
    def set_animation(self, position, animation_name):
        pattern = Pattern(int(position[0]) + 256, int(position[1]) + 144, animation_name)
        self._backpatterns.append(pattern)

    def change_animation(self, position, new_animation):
        for pattern in self._backpatterns:
            if pattern.x == position[0] and pattern.y == position[1]:
                if new_animation is None:
                    self._backpatterns.remove(pattern)
                else:
                    pattern.animation_name = new_animation

        for pattern in self._forepatterns:
            if pattern.x == position[0] and pattern.y == position[1]:
                if new_animation is None:
                    self._forepatterns.remove(pattern)
                else:
                    pattern.animation_name = new_animation

    def run(self):
        self._run_animation(self._backpatterns)
        self._run_animation(self._forepatterns)

    def render(self):
        # Source rendering
        self._tmp_surface.blit(self._source,
                               (self._player.x - 128, self._player.y - 72),
                               (self._player.x - 128, self._player.y - 72, 256, 144))

        # Backpattern rendering
        for pattern in self._backpatterns:
            animation = self._animations.get(pattern.animation_name)
            img = animation.images.get(str(animation.frames[animation.active_frame].id))
            self._tmp_surface.blit(img, (
                pattern.x + animation.frames[animation.active_frame].offset_x,
                pattern.y + animation.frames[animation.active_frame].offset_y))

        # Player rendering
        self._player.render(self._tmp_surface)

        # Enemies rendering
        for enemy in self._enemies:
            enemy.render(self._tmp_surface)

        # Crushers rendering
        for crusher in self._crushers:
            crusher.render(self._tmp_surface)

        # Powerup rendering
        self._powerups.render(self._tmp_surface)

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
                                   (pattern.x + animation.frames[animation.active_frame].offset_x,
                                    pattern.y + animation.frames[animation.active_frame].offset_y))

        # Viewport rendering
        self._screen.virt.blit(self._tmp_surface, (0, 0),
                               (self._player.x - 128, self._player.y - 72, 256, 144))

        # Board rendering
        self._board.render(self._screen.virt)

        # Debug information
        '''
        pygame.draw.rect(self._screen.virt, (30, 30, 30), (0, 0, 100, 20), 0)
        text = self._font_white.get(('x:' + str(self._player.x - 264) + ' y:' + str(self._player.y - 152)), 100)
        self._screen.virt.blit(text, (5, 5))
        '''

    @property
    def speed(self):
        return self._speed
