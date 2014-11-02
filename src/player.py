class Player(object):

    def __init__(self, rmngr, current_level):
        self.sprites = []
        player = [
            'player0', 'player1', 'player2', 'player3',
            'player4', 'player5', 'player6', 'player7',
            'player8', 'player9', 'player10', 'player11',
            'player12', 'player13', 'player14'
        ]

        for p in xrange(0, len(player)):
            self.sprites.insert(p, rmngr.get(player[p]))

        self.w = self.sprites[0].get_width()
        self.h = self.sprites[0].get_height()
        self.x = current_level.start_point[0] * current_level.map.tilewidth
        self.y = current_level.start_point[1] * current_level.map.tileheight
        self.absolute_x = self.x
        self.absolute_y = self.y
        self.animation = 0
        self.direction = 1
