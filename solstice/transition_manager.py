import pygame


class TransitionManager(object):
    def __init__(self, resource_manager):
        self._resource_manager = resource_manager
        self._transitions = self._init_transitions()
        self._transition = None

    '''
    Private methods
    '''

    def _init_transitions(self):
        transition_factory = TransitionFactory(self._resource_manager)
        transition_list = ['circles_in', 'squares_in', 'dummy']
        return {transition: transition_factory.get(transition) for transition in transition_list}

    '''
    Public methods
    '''

    def set(self, transition_name):
        self._transition = self._transitions[transition_name]

    def start(self):
        self._transition.start()

    def run(self):
        self._transition.run()

    def render(self, screen):
        self._transition.render(screen)

    @property
    def status(self):
        return self._transition.status

    @status.setter
    def status(self, value):
        self._transition.status = value


class TransitionFactory(object):
    def __init__(self, resource_manager):
        self._resource_manager = resource_manager

    '''
    Public methods
    '''

    def get(self, transition_type):
        if transition_type == 'circles_in':
            sprites = [self._resource_manager.get('circle_transition' + str(index))
                       for index in xrange(6, -1, -1)]
            return TransitionCirclesIn(6, sprites)

        if transition_type == 'squares_in':
            sprites = [self._resource_manager.get('transition' + str(index))
                       for index in xrange(8, -1, -1)]
            return TransitionSquaresIn(32, sprites)

        if transition_type == 'dummy':
            return TransitionDummy(0, None)


class Transition(object):
    IDLE = 0x01
    STARTING = 0x02
    FINISHED = 0x04

    def __init__(self, total_frames, sprites):
        self._status = Transition.IDLE
        self._total_frames = total_frames
        self._sprites = sprites
        self._frame = -1

    '''
    Public methods
    '''

    def start(self):
        self._frame = -1
        self._status = Transition.STARTING

    def render(self, screen):
        raise NotImplementedError('Not yet implemented')

    def run(self):
        if self._status == Transition.IDLE or self._status == Transition.FINISHED:
            return

        if self._status == Transition.STARTING:
            if self._frame < self._total_frames:
                self._frame += 1
            else:
                self._status = Transition.FINISHED

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value


class TransitionDummy(Transition):
    def __init__(self, total_frames, sprites):
        super(TransitionDummy, self).__init__(total_frames, sprites)

    def render(self, screen):
        pass


class TransitionCirclesIn(Transition):
    def __init__(self, total_frames, sprites):
        super(TransitionCirclesIn, self).__init__(total_frames, sprites)

    '''
    Public methods
    '''

    def render(self, screen):
        if not (self._status == Transition.IDLE or self._status == Transition.FINISHED):
            for y in xrange(0, 24):
                for x in xrange(0, 32):
                    screen.virtual_screen.blit(self._sprites[self._frame], (x * 8, y * 8))


class TransitionSquaresIn(Transition):
    def __init__(self, total_frames, sprites):
        super(TransitionSquaresIn, self).__init__(total_frames, sprites)
        self._offset = 256
        self._matrix = [
            [1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 8, 8],
            [0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 8],
            [0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8],
            [0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 8],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        ]

    '''
    Public methods
    '''

    def start(self):
        super(TransitionSquaresIn, self).start()
        self._offset = 256

    def run(self):
        super(TransitionSquaresIn, self).run()
        if not (self._status == Transition.IDLE or self._status == Transition.FINISHED):
            if self._offset > -256:
                self._offset -= 16

    def render(self, screen):
        if not (self._status == Transition.IDLE or self._status == Transition.FINISHED):
            pygame.draw.rect(screen.virtual_screen, (0, 0, 0), (0, 0, self._offset, 192))
            for y in xrange(0, 19):
                for x in xrange(0, 19):
                    screen.virtual_screen.blit(self._sprites[self._matrix[y][x]],
                                               (self._offset + (x * 16), y * 16))
