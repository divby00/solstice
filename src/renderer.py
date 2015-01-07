import pygame


class Pattern(object):

    def __init__(self, x, y, animation_name):
        self.x = x
        self.y = y
        self.animation_name = animation_name


class Renderer(object):

    def __init__(self, context):
        self.screen = context.screen
        self.level = context.current_level
        self.player = context.player
        self.items = context.items
        self.animations = context.animations
        self.particlesmanager = context.particlesmanager
        self.player = context.player
        self.board = context.board
        self.speed = 4, 4
        self.start_point = self.__get_start_point()
        self.source = self.__init_source_image()
        self.backpatterns = []
        self.forepatterns = []
        self.__init_patterns()
        self.tmp = pygame.Surface((self.source.get_width(), self.source.get_height())).convert()
        self.tmp.fill((0, 0, 0, 0))

    def __get_start_point(self):
        return ((self.level.start_point[0]) + 256 + 8) - 128, ((self.level.start_point[1]) + 144 + 8) - 72

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

    def __init_patterns(self):

        animations = self.level.animated_tiles

        for a in animations:
            data = a.split(' ')
            zindex = data[0]
            animx = data[1]
            animy = data[2]
            animname = animations.get(a)

            if zindex == '0':
                self.backpatterns.append(Pattern(int(animx) + 256, int(animy) + 144, animname))
            else:
                self.forepatterns.append(Pattern(int(animx) + 256, int(animy) + 144, animname))

    def change_animation(self, position, new_anim):
        for b in self.backpatterns:
            if b.x == position[0] and b.y == position[1]:
                if new_anim is None:
                    self.backpatterns.remove(b)
                else:
                    b.animation_name = new_anim
        for b in self.forepatterns:
            if b.x == position[0] and b.y == position[1]:
                if new_anim is None:
                    self.forepatterns.remove(b)
                else:
                    b.animation_name = new_anim

    def run(self):
        for b in self.backpatterns:
            anim = self.animations.get(b.animation_name)

            if anim.counter < anim.frames[anim.active_frame].duration:
                anim.counter += 1
            else:
                anim.counter = 0

                if anim.active_frame < len(anim.frames) - 1:
                    anim.active_frame += 1
                else:
                    anim.active_frame = 0

        for b in self.forepatterns:
            anim = self.animations.get(b.animation_name)

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
        self.tmp.blit(self.source,
                      (self.player.x - 128, self.player.y - 72),
                      (self.player.x - 128, self.player.y - 72, 256, 144))

        # Backpattern rendering
        for b in self.backpatterns:
            anim = self.animations.get(b.animation_name)
            img = anim.images.get(str(anim.frames[anim.active_frame].id))
            self.tmp.blit(img, (b.x + anim.frames[anim.active_frame].offsetx, b.y + anim.frames[anim.active_frame].offsety))

        # Player rendering
        self.player.render(self.tmp)

        # Particles rendering
        self.particlesmanager.render(self.tmp)

        # Forepattern rendering
        for b in self.forepatterns:
            anim = self.animations.get(b.animation_name)
            img = anim.images.get(str(anim.frames[anim.active_frame].id))
            self.tmp.blit(img, (b.x + anim.frames[anim.active_frame].offsetx, b.y + anim.frames[anim.active_frame].offsety))

        # Viewport rendering
        self.screen.virt.blit(self.tmp, (0, 0), (self.player.x - 128, self.player.y - 72, 256, 144))

        # Board rendering
        self.board.render(self.screen.virt)
