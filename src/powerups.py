import random

circular_motion_lookup_table = [
    (1, 0), (1, 1), (1, 1), (0, 1), (0, 1), (-1, 1), (-1, 1), (-1, 0),
    (-1, 0), (-1, -1), (-1, -1), (0, -1), (0, -1), (1, -1), (1, -1), (1, 0)
]


class Powerups(object):
    def __init__(self):
        self._powerups = []

    def run(self):
        for powerup in self._powerups:
            active = powerup.run()
            if not active:
                self._powerups.remove(powerup)

    def render(self, surface):
        for powerup in self._powerups:
            powerup.render(surface)

    def add(self, powerup):
        self._powerups.append(powerup)

    @property
    def powerups(self):
        return self._powerups


class PowerupBuilder(object):
    LIFE = 0
    BEAM = 1
    THRUST = 2

    @staticmethod
    def build(position, game_context):
        # Random powerup
        selected_powerup = random.randint(0, 2)
        if selected_powerup == PowerupBuilder.LIFE:
            game_context.powerups.add(LifePowerup(position, game_context))
        elif selected_powerup == PowerupBuilder.BEAM:
            game_context.powerups.add(BeamPowerup(position, game_context))
        elif selected_powerup == PowerupBuilder.THRUST:
            game_context.powerups.add(ThrustPowerup(position, game_context))


class Powerup(object):
    APPEARING = 0
    ON_SCENE = 1
    DISAPPEARING = 2

    def __init__(self, position, game_context):
        self._active = True
        self._status = Powerup.APPEARING
        self._frame = 0
        self._anim_frame = 0
        self._spr_frame = 0
        self._x = position[0] + 3
        self._y = position[1] + 3
        self._game_context = game_context
        self._sprites = None
        self._transition_sprites = self._get_transition_sprites()

    def _get_transition_sprites(self):
        return [self._game_context.resource_manager.get(''.join(['powerup_transition_0', str(x)]))
                for x in range(0, 3)]

    def run(self):
        if self._active:
            if 0 <= self._frame < 4:
                self._status = Powerup.APPEARING
            elif 4 <= self._frame < 44:
                self._status = Powerup.ON_SCENE
                self._x += circular_motion_lookup_table[self._anim_frame][0]
                self._y += circular_motion_lookup_table[self._anim_frame][1]
                self._anim_frame += 1
                self._spr_frame += 1
                if self._spr_frame == 3:
                    self._spr_frame = 0
                if self._anim_frame == 16:
                    self._anim_frame = 0
            elif 44 <= self._frame < 48:
                self._status = Powerup.DISAPPEARING
            else:
                self._active = False

            self._frame += 1

        return self._active

    def render(self, surface):
        if self._active:
            if self._status == Powerup.APPEARING:
                surface.blit(self._transition_sprites[2], (256 + self._x, 144 + self._y))
            if self._status == Powerup.ON_SCENE:
                surface.blit(self._sprites[self._spr_frame], (256 + self._x, 144 + self._y))


class ThrustPowerup(Powerup):
    def __init__(self, position, game_context):
        super(ThrustPowerup, self).__init__(position, game_context)
        self._sprites = [game_context.resource_manager.get(''.join(['powerup_thrust_0', str(x)]))
                         for x in range(0, 3)]


class BeamPowerup(Powerup):
    def __init__(self, position, game_context):
        super(BeamPowerup, self).__init__(position, game_context)
        self._sprites = [game_context.resource_manager.get(''.join(['powerup_beam_0', str(x)]))
                         for x in range(0, 3)]


class LifePowerup(Powerup):
    def __init__(self, position, game_context):
        super(LifePowerup, self).__init__(position, game_context)
        self._sprites = [game_context.resource_manager.get(''.join(['powerup_life_0', str(x)]))
                         for x in range(0, 3)]
