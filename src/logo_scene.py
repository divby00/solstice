import pygame

import scene


class LogoScene(scene.Scene):
    LOGO_DELAY = 1500

    def __init__(self, context, name='logo', scene_speed=25):
        super(LogoScene, self).__init__(context, name, scene_speed)
        self._sound_player = context.sound_player
        self._logo = context.resource_manager.get('logo')
        self._logo_sound = self._sound_player.load_sample(['logo_sound'])
        self._dither_sprites = [context.resource_manager.get('dither' + str(index))
                                for index in xrange(0, 6)]
        self._dithering_frame = None
        self._fading = 0
        self._playing = False

    '''
    Public methods
    '''

    def on_start(self):
        self._dithering_frame = len(self._dither_sprites)
        self._fading = 0
        self._playing = False

    def on_quit(self):
        pass

    def run(self):

        if not self._playing:
            self._playing = True
            self._sound_player.play_sample('logo_sound')

        if self._dithering_frame > -1 and self._fading == 0:
            self._dithering_frame -= 1

        if self._dithering_frame == -1 and self._fading == 0:
            self._dithering_frame = 0
            self._fading = 1
            pygame.time.delay(LogoScene.LOGO_DELAY)

        if self._dithering_frame < len(self._dither_sprites) and self._fading == 1:
            self._dithering_frame += 1

        # Exit condition
        if self._dithering_frame == len(self._dither_sprites) and self._fading == 1:
            self._scene_manager.set('intro')

    def render(self, screen):

        if self._dithering_frame < len(self._dither_sprites):
            # TODO Take to reuse as a centered drawing function
            screen.virt.blit(self._logo, (128 - (self._logo.get_width() / 2),
                                          96 - (self._logo.get_height() / 2)))

        for a in xrange(0, 192, 8):
            for i in xrange(0, 256, 8):
                if self._dithering_frame < len(self._dither_sprites):
                    screen.virt.blit(self._dither_sprites[self._dithering_frame], (i, a))
                else:
                    screen.virt.fill((0, 0, 0, 0))
