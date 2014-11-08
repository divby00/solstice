import scene
import pygame


class LogoScene(scene.Scene):

    LOGO_DELAY = 1500

    def __init__(self, resourcemanager, scene_speed=30):
        super(LogoScene, self).__init__(resourcemanager, scene_speed)
        self.logo = resourcemanager.get('logo')
        self.logo_sound = resourcemanager.get('logo_sound')
        self.dither = []
        dither_images = [
            'dither0', 'dither1', 'dither2',
            'dither3', 'dither4', 'dither5'
        ]

        for d in xrange(0, len(dither_images)):
            self.dither.insert(d, resourcemanager.get(dither_images[d]))

        self.dither_anim = len(self.dither)
        self.fading = 0
        self.playing = False

    def run(self):

        if not self.playing:
            self.playing = True
            pygame.mixer.Sound(self.logo_sound).play()

        if self.dither_anim > -1 and self.fading == 0:
            self.dither_anim -= 1

        if self.dither_anim == -1 and self.fading == 0:
            self.dither_anim = 0
            self.fading = 1
            pygame.time.delay(LogoScene.LOGO_DELAY)

        if self.dither_anim < len(self.dither) and self.fading == 1:
            self.dither_anim += 1

        #Exit condition
        if self.dither_anim == len(self.dither) and self.fading == 1:
            self.running = False

    def render(self, scr):

        if self.dither_anim < len(self.dither):
            scr.virt.blit(self.logo,
                         (128-(self.logo.get_width()/2),
                          96-(self.logo.get_height()/2)))

        for a in xrange(0, 192, 8):
            for i in xrange(0, 256, 8):
                if self.dither_anim < len(self.dither):
                    scr.virt.blit(self.dither[self.dither_anim], (i, a))
                else:
                    scr.virt.fill((0, 0, 0, 0))
