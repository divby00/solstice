import pygame
import scene
import i18n


class MenuScene(scene.Scene):

    def __init__(self, resourcemanager, scene_speed=30):
        super(MenuScene, self).__init__(resourcemanager, scene_speed)
        self.menu = resourcemanager.get('menu')
        self.panel = []
        panel = ['panel0', 'panel1', 'panel2',
                 'panel3', 'panel4', 'panel5',
                 'panel6', 'panel7', 'panel8']

        for p in xrange(0, len(panel)):
            self.panel.insert(p, resourcemanager.get(panel[p]))

        self.text = self.font.get('Solstice')
        self.text_0 = self.font.get(i18n._('Test Text'))
        self.pnl_srf = pygame.Surface((128, 80))
        self.pnl_srf = self.pnl_srf.convert_alpha()
        self.pnl_srf.fill((0, 0, 0, 0))
        img = -1

        self.music = resourcemanager.get('menu_song')

        for a in xrange(0, 80, 8):
            for i in xrange(0, 128, 8):
                if a == 0 and i == 0:
                    img = 0
                if a == 0 and i > 0 and i < 120:
                    img = 1
                if a == 0 and i == 120:
                    img = 2
                if a > 0 and a < 72 and i == 0:
                    img = 3
                if a > 0 and a < 72 and i > 0 and i < 120:
                    img = 4
                if a > 0 and a < 72 and i == 120:
                    img = 5
                if a == 72 and i == 0:
                    img = 6
                if a == 72 and i > 0 and i < 120:
                    img = 7
                if a == 72 and i == 120:
                    img = 8

                self.pnl_srf.blit(self.panel[img], (i, a))
                self.pnl_srf.blit(self.text, (32, 16))

    def run(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            pygame.mixer.music.stop()
            self.running = False

    def render(self, scr):
        scr.virt.blit(self.menu, (128-self.menu.get_width()/2, 0))