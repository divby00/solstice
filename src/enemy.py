class Enemy(object):
    def __init__(self):
        pass


class Jellyfish(Enemy):
    def __init__(self):
        super(Jellyfish, self).__init__()


class EnemyBuilder(object):
    @staticmethod
    def build(game_context):
        enemy_data = game_context.current_level.map.enemy_data
        for k in enemy_data.keys():
            print(k)
