import ConfigParser


class Configuration(object):

    OPT_DATA_PATH = 'data path'
    OPT_LOCALE_PATH = 'locale path'
    OPT_SCREEN_WIDTH = 'screen width'
    OPT_SCREEN_HEIGHT = 'screen height'
    OPT_FULLSCREEN = 'fullscreen'
    OPT_SOUND = 'sound'
    OPT_MUSIC = 'music'
    OPT_SOUND_VOL = 'sound volume'
    OPT_MUSIC_VOL = 'music volume'

    ''' Default values '''
    DATA_PATH = './'
    LOCALE_PATH = 'locale'
    SECTION = ['Paths', 'Graphics', 'Sound']
    SCREEN_SIZE = [1024, 768]
    FULLSCREEN = False
    SOUND = True
    MUSIC = True
    SOUND_VOLUME = 10
    MUSIC_VOLUME = 10
    CFGFILE_NAME = 'solstice.cfg'

    def __init__(self):
        self.config_parser = ConfigParser.ConfigParser()
        parsed_file = self.config_parser.read([Configuration.CFGFILE_NAME])

        if len(parsed_file) > 0:
            self.data_path = self.config_parser.get(Configuration.SECTION[0],
                                                    Configuration.OPT_DATA_PATH)
            self.locale_path = self.config_parser.get(Configuration.SECTION[0],
                                                      Configuration.OPT_LOCALE_PATH)
            w = self.config_parser.getint(Configuration.SECTION[1],
                                          Configuration.OPT_SCREEN_WIDTH)
            h = self.config_parser.getint(Configuration.SECTION[1],
                                          Configuration.OPT_SCREEN_HEIGHT)
            self.fullscreen = self.config_parser.getboolean(Configuration.SECTION[1],
                                                            Configuration.OPT_FULLSCREEN)
            self.sound = self.config_parser.getboolean(Configuration.SECTION[2],
                                                       Configuration.OPT_SOUND)
            self.music = self.config_parser.getboolean(Configuration.SECTION[2],
                                                       Configuration.OPT_MUSIC)
            self.sound_vol = self.config_parser.getint(Configuration.SECTION[2],
                                                       Configuration.OPT_SOUND_VOL)
            self.music_vol = self.config_parser.getint(Configuration.SECTION[2],
                                                       Configuration.OPT_MUSIC_VOL)
            self.screen_size = (w, h)

        else:
            for section in Configuration.SECTION:
                self.config_parser.add_section(section)

            self.config_parser.set(Configuration.SECTION[0],
                                   Configuration.OPT_DATA_PATH,
                                   Configuration.DATA_PATH)
            self.config_parser.set(Configuration.SECTION[0],
                                   Configuration.OPT_LOCALE_PATH,
                                   Configuration.LOCALE_PATH)
            self.config_parser.set(Configuration.SECTION[1],
                                   Configuration.OPT_SCREEN_WIDTH,
                                   Configuration.SCREEN_SIZE[0])
            self.config_parser.set(Configuration.SECTION[1],
                                   Configuration.OPT_SCREEN_HEIGHT,
                                   Configuration.SCREEN_SIZE[1])
            self.config_parser.set(Configuration.SECTION[1],
                                   Configuration.OPT_FULLSCREEN,
                                   Configuration.FULLSCREEN)
            self.config_parser.set(Configuration.SECTION[2],
                                   Configuration.OPT_SOUND,
                                   Configuration.SOUND)
            self.config_parser.set(Configuration.SECTION[2],
                                   Configuration.OPT_MUSIC,
                                   Configuration.MUSIC)
            self.config_parser.set(Configuration.SECTION[2],
                                   Configuration.OPT_SOUND_VOL,
                                   Configuration.SOUND_VOLUME)
            self.config_parser.set(Configuration.SECTION[2],
                                   Configuration.OPT_MUSIC_VOL,
                                   Configuration.MUSIC_VOLUME)

            self.save()

            self.data_path = Configuration.DATA_PATH
            self.locale_path = Configuration.LOCALE_PATH
            self.screen_size = (Configuration.SCREEN_SIZE[0],
                                Configuration.SCREEN_SIZE[1])
            self.fullscreen = Configuration.FULLSCREEN
            self.sound = Configuration.SOUND
            self.music = Configuration.MUSIC
            self.sound_vol = Configuration.SOUND_VOLUME
            self.music_vol = Configuration.MUSIC_VOLUME

    def save(self):
        with open(Configuration.CFGFILE_NAME, 'wb') as config_file:
            self.config_parser.write(config_file)
