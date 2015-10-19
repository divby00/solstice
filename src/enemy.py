from gettext import gettext as _
import math


class Enemy(object):
    def __init__(self, type):
        self.x = 0
        self.y = 0
        self.active = False
        self.type = type


class Jellyfish(Enemy):
    def __init__(self):
        super(Jellyfish, self).__init__('jellyfish')


class Devil(Enemy):
    def __init__(self):
        super(Devil, self).__init__('devil')


class EnemyUnknownException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class EnemyBuilder(object):
    @staticmethod
    def build(game_context):
        results = []
        enemy_frequency = [
            'jellyfish_frequency',
            'devil_frequency'
        ]

        try:
            enemy_data = game_context.current_level.map.enemy_data
            max_enemies = 0

            # Get max enemies
            for k, v in enemy_data.iteritems():
                if 'max_enemies' in k:
                    max_enemies = int(v)

            assert max_enemies > 0

            # Get total = 100%
            total = 0
            enemy_amount = {}
            for k, v in enemy_data.iteritems():
                if k in enemy_frequency:
                    total += int(v)
                    enemy_amount[k] = math.floor((max_enemies * int(v)) / 100)

            assert total == 100

            # Build enemies
            for k, v in enemy_amount.iteritems():
                for e in range(int(v)):
                    if 'jellyfish_frequency' in k:
                        enemy = Jellyfish()
                    elif 'devil_frequency' in k:
                        enemy = Devil()
                    else:
                        raise EnemyUnknownException(_('Unable to find enemy %s' % k))
                    results.append(enemy)

        except EnemyUnknownException as e:
            print(e.value)

        return results
