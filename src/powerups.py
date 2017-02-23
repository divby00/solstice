import random

circular_motion_lookup_table = [
    (1, 0), (1, 1), (1, 1), (0, 1), (0, 1), (-1, 1), (-1, 1), (-1, 0),
    (-1, 0), (-1, -1), (-1, -1), (0, -1), (0, -1), (1, -1), (1, -1), (1, 0)
]


class Powerups(object):
    def __init__(self, player):
        self._powerups = []
        self._player = player

    def run(self):
        for powerup in self._powerups:
            active = powerup.run(self._player)
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
        selected_powerup = random.randint(0, 7)
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
                for x in range(0, 4)]

    def _run_animation_logic(self):
        if 0 <= self._frame < 3:
            self._status = Powerup.APPEARING
        elif 3 <= self._frame < 43:
            self._status = Powerup.ON_SCENE
            self._x += circular_motion_lookup_table[self._anim_frame][0]
            self._y += circular_motion_lookup_table[self._anim_frame][1]
            self._anim_frame += 1
            self._spr_frame += 1
            if self._spr_frame >= 4:
                self._spr_frame = 0
            if self._anim_frame >= 16:
                self._anim_frame = 0
        elif self._frame == 43:
            self._status = Powerup.DISAPPEARING
            self._anim_frame = 3
        elif 43 < self._frame < 47:
            self._anim_frame -= 1
        else:
            self._active = False

        self._frame += 1

    def _run_apply_powerup(self, player):
        if player.x - 256 + 8 >= self._x and player.x - 256 - 8 <= self._x + 10 \
                and player.y - 144 + 8 >= self._y and player.y - 144 - 8 <= self._y + 10:
            self.apply(player)
            self._active = False

    def run(self, player):
        if self._active:
            self._run_animation_logic()
            self._run_apply_powerup(player)

        return self._active

    def render(self, surface):
        if self._active:
            if self._status == Powerup.APPEARING:
                surface.blit(self._transition_sprites[self._frame], (256 + self._x, 144 + self._y))
            if self._status == Powerup.ON_SCENE:
                surface.blit(self._sprites[self._spr_frame], (256 + self._x, 144 + self._y))
            if self._status == Powerup.DISAPPEARING:
                surface.blit(self._transition_sprites[self._anim_frame],
                             (256 + self._x, 144 + self._y))

    def apply(self, player):
        raise NotImplementedError('Implement this method')


class ThrustPowerup(Powerup):
    THRUST_LIMIT = 107

    def __init__(self, position, game_context):
        super(ThrustPowerup, self).__init__(position, game_context)
        self._sprites = [game_context.resource_manager.get(''.join(['powerup_thrust_0', str(x)]))
                         for x in range(0, 4)]

    def apply(self, player):
        player.thrust += 5
        if player.thrust > ThrustPowerup.THRUST_LIMIT:
            player.thrust = ThrustPowerup.THRUST_LIMIT
        self._game_context.sound_player.play_sample('powerup')


class BeamPowerup(Powerup):
    BULLETS_LIMIT = 107

    def __init__(self, position, game_context):
        super(BeamPowerup, self).__init__(position, game_context)
        self._sprites = [game_context.resource_manager.get(''.join(['powerup_beam_0', str(x)]))
                         for x in range(0, 4)]

    def apply(self, player):
        player.bullets += 5
        if player.bullets > BeamPowerup.BULLETS_LIMIT:
            player.bullets = BeamPowerup.BULLETS_LIMIT
        self._game_context.sound_player.play_sample('powerup')


class LifePowerup(Powerup):
    LIFE_LIMIT = 100

    def __init__(self, position, game_context):
        super(LifePowerup, self).__init__(position, game_context)
        self._sprites = [game_context.resource_manager.get(''.join(['powerup_life_0', str(x)]))
                         for x in range(0, 4)]

    def apply(self, player):
        player.life += 10
        if player.life > LifePowerup.LIFE_LIMIT:
            player.life = LifePowerup.LIFE_LIMIT
        self._game_context.sound_player.play_sample('powerup')
