import pygame


class Scroll(object):

    def __init__(self, level, player):
        self.level = level
        self.player = player
        self.start_point = self.__get_start_point()
        self.source = self.__init_source_image()
        self.tmp = pygame.Surface((self.source.get_width(), self.source.get_height())).convert()
        self.tmp.fill((0, 0, 0, 0))
        self.img = pygame.Surface((256, 144)).convert()
        self.img.fill((0, 0, 0))

    def __get_start_point(self):
        return ((self.level.start_point[0] * 8) + 256 + 8) - 128, ((self.level.start_point[1] * 8) + 144 + 8) - 72

    def __init_source_image(self):
        level_size = self.level.map.width_pixels, self.level.map.height_pixels
        back = pygame.Surface((level_size[0] + 512, level_size[1] + 288)).convert()
        back.fill((0, 0, 0))
        back_img = self.level.back
        walls = pygame.Surface(level_size).convert_alpha()
        walls.fill((0, 0, 0, 0))

        # Draw the back image in the buffer
        for a in xrange(0, back.get_height(), back_img.get_height()):
            for i in xrange(0, back.get_width(), back_img.get_width()):
                back.blit(back_img, (i, a))

        # Draw the background in the buffer
        for l in self.level.layers:
            if l.name == 'background':
                posx = posy = 0
                for a in xrange(0, level_size[1] / 8):
                    for i in xrange(0, level_size[0] / 8):
                        gid = l.get_gid(i, a)
                        if gid > 0:
                            walls.blit(self.level.tiles[gid - 1].srfc, (posx, posy))
                        posx += 8
                    posx = 0
                    posy += 8

        # Draw the walls in the buffer
        for l in self.level.layers:
            if l.name == 'walls':
                posx = posy = 0
                for a in xrange(0, level_size[1] / 8):
                    for i in xrange(0, level_size[0] / 8):
                        gid = l.get_gid(i, a)
                        if gid > 0:
                            walls.blit(self.level.tiles[gid - 1].srfc, (posx, posy))
                        posx += 8
                    posx = 0
                    posy += 8

        x = (back.get_width() / 2) - (walls.get_width() / 2)
        y = (back.get_height() / 2) - (walls.get_height() / 2)
        back.blit(walls, (x, y))
        return back

    def get_frame(self):
        self.tmp.fill((100, 0, 0))
        # Source rendering
        self.tmp.blit(self.source,
                      (self.player.x - 128, self.player.y - 72),
                      (self.player.x - 128, self.player.y - 72, 256, 144))

        # Backpatterns
        level_size = self.level.map.width_pixels, self.level.map.height_pixels

        '''
        for l in self.level.layers:
            if l.name == 'backpatterns':
                posx = posy = 0
                for a in xrange(0, level_size[1] / 8):
                    for i in xrange(0, level_size[0] / 8):
                        gid = l.get_gid(i, a)
                        if gid > 0:
                            self.tmp.blit(self.level.tiles[gid - 1].srfc, (posx + 256, posy + 144))
                        posx += 8
                    posx = 0
                    posy += 8
        '''

        # Player rendering
        self.tmp.blit(self.player.sprites[self.player.animation], (self.player.x - 8, self.player.y - 8))

        # Forepatterns
        '''
        for l in self.level.layers:
            if l.name == 'forepatterns':
                posx = posy = 0
                for a in xrange(0, level_size[1] / 8):
                    for i in xrange(0, level_size[0] / 8):
                        gid = l.get_gid(i, a)
                        if gid > 0:
                            self.tmp.blit(self.level.tiles[gid - 1].srfc, (posx + 256, posy + 144))
                        posx += 8
                    posx = 0
                    posy += 8
        '''

        # Viewport rendering
        self.img.blit(self.tmp, (0, 0), (self.player.x - 128, self.player.y - 72, 256, 144))

        # Add quadrant lines
        pygame.draw.line(self.img, (200, 200, 0), (128, 0), (128, 144))
        pygame.draw.line(self.img, (200, 200, 0), (0, 72), (256, 72))
        return self.img
