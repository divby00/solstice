import pygame


class SoundPlayer(object):
    def __init__(self, context):
        self.context = context
        self.music = self.context.cfg.music
        self.sound = self.context.cfg.sound
        self.song = None
        self.samples = {}

    def play(self, sound):
        if self.sound:
            sound.play()

    def load_sample(self, sample_list):
        if self.sound:
            for s in sample_list:
                self.samples[s] = self.context.resourcemanager.get(s)

    def load_music(self, song_name):
        if self.music:
            self.song = self.context.resourcemanager.get(song_name)
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.music.load(self.song)

    def play_sample(self, sample_name):
        if self.sound:
            self.samples[sample_name].play()

    def play_music(self):
        if self.music:
            pygame.mixer.music.play(-1)

    def stop_music(self):
        if self.music:
            pygame.mixer.music.stop()

    def stop(self):
        if self.sound:
            pygame.mixer.stop()
