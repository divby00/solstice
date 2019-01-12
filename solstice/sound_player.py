import pygame


class SoundPlayer(object):
    def __init__(self, context):
        self._context = context
        self._music = self._context.config.music
        self._sound = self._context.config.sound
        self._song = None
        self._samples = {}

    '''
    Public methods
    '''

    def play(self, sound):
        if self._sound:
            sound.play()

    def load_sample(self, sample_list):
        if self._sound:
            for sample in sample_list:
                self._samples[sample] = self._context.resource_manager.get(sample)

    def load_music(self, song_name):
        if self._music:
            self._song = self._context.resource_manager.get(song_name)
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.music.load(self._song)

    def play_sample(self, sample_name):
        if self._sound:
            self._samples[sample_name].play()

    def play_music(self):
        if self._music:
            pygame.mixer.music.play(-1)

    def stop_music(self):
        if self._music:
            pygame.mixer.music.stop()

    def stop(self):
        if self._sound:
            pygame.mixer.stop()
