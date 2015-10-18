import pygame


class Board(object):
    def __init__(self, context, player):
        self.player = player
        self.board = context.resourcemanager.get('board')
        self.bluebar = []
        self.greenbar = []
        self.redbar = []
        self.dronelife = []

        for i in xrange(0, 3):
            self.bluebar.insert(i, context.resourcemanager.get('bluebar' + str(i)))
            self.greenbar.insert(i, context.resourcemanager.get('greenbar' + str(i)))
            self.redbar.insert(i, context.resourcemanager.get('redbar' + str(i)))

        for i in xrange(0, 9):
            self.dronelife.insert(i, context.resourcemanager.get('playerhit' + str(i)))

    def render(self, screen):
        pygame.draw.rect(self.board, (0, 0, 0), (136, 17, 112, 22), 0)
        pygame.draw.rect(self.board, (0, 0, 0), (44, 16, 16, 16), 0)
        pygame.draw.rect(self.board, (0, 0, 0), (12, 16, 16, 16), 0)

        # Render player life
        if self.player.life < 0:
            self.player.life = 0

        life = int(round(self.player.life))
        di = (life * 8) / 100
        self.board.blit(self.dronelife[8 - di], (44, 16))

        # Render thrust bar
        selected_bar = None

        if self.player.thrust < 0:
            self.player.thrust = 0

        thrust = int(round(self.player.thrust))

        if thrust > 70:
            selected_bar = self.bluebar
        elif 35 < thrust <= 70:
            selected_bar = self.greenbar
        else:
            selected_bar = self.redbar

        self.board.blit(selected_bar[0], (136, 17))
        for i in xrange(0, thrust):
            self.board.blit(selected_bar[1], (138 + i, 17))
        self.board.blit(selected_bar[2], (138 + thrust, 17))

        # Render bullets bar
        if self.player.bullets < 0:
            self.player.bullets = 0

        bullets = int(round(self.player.bullets))

        if bullets > 70:
            selected_bar = self.bluebar
        elif 35 < bullets <= 70:
            selected_bar = self.greenbar
        else:
            selected_bar = self.redbar

        self.board.blit(selected_bar[0], (136, 25))
        for i in xrange(0, bullets):
            self.board.blit(selected_bar[1], (138 + i, 25))
        self.board.blit(selected_bar[2], (138 + bullets, 25))

        # Render time bar TODO

        # Render selected item
        if self.player.selected_item is not None:
            item = self.player.selected_item
            self.board.blit(item.sprite, (12, 16))

        screen.blit(self.board, (0, 144))
