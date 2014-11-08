import ConfigParser


class ConfigurationFileError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


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
    OPT_CONTROL_TYPE = 'type'
    OPT_KEY_UP = 'key up'
    OPT_KEY_DOWN = 'key down'
    OPT_KEY_LEFT = 'key left'
    OPT_KEY_RIGHT = 'key right'
    OPT_KEY_ACTION_1 = 'key action 1'
    OPT_KEY_ACTION_2 = 'key action 2'

    ''' Default values '''
    DATA_PATH = './'
    LOCALE_PATH = 'locale'
    SECTION = ['Paths', 'Graphics', 'Sound', 'Control']
    SCREEN_SIZE = [1024, 768]
    FULLSCREEN = False
    SOUND = True
    MUSIC = True
    SOUND_VOLUME = 10
    MUSIC_VOLUME = 10
    CFGFILE_NAME = 'solstice.cfg'
    CONTROL_TYPE = 'keyboard'
    KEY_UP = 'a'
    KEY_DOWN = 'b'
    KEY_LEFT = 'c'
    KEY_RIGHT = 'd'
    KEY_ACTION_1 = 'e'
    KEY_ACTION_2 = 'f'

    def __init__(self):
        try:
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

                self.control_type = self.config_parser.get(Configuration.SECTION[3],
                                                           Configuration.OPT_CONTROL_TYPE)
                self.key_up = self.config_parser.get(Configuration.SECTION[3],
                                                     Configuration.OPT_KEY_UP)
                self.key_down = self.config_parser.get(Configuration.SECTION[3],
                                                       Configuration.OPT_KEY_DOWN)
                self.key_left = self.config_parser.get(Configuration.SECTION[3],
                                                       Configuration.OPT_KEY_LEFT)
                self.key_right = self.config_parser.get(Configuration.SECTION[3],
                                                        Configuration.OPT_KEY_RIGHT)
                self.key_act1 = self.config_parser.get(Configuration.SECTION[3],
                                                       Configuration.OPT_KEY_ACTION_1)
                self.key_act2 = self.config_parser.get(Configuration.SECTION[3],
                                                       Configuration.OPT_KEY_ACTION_2)
            else:
                self.__set_default_values()

        except:
            self.__set_default_values()

    def __set_default_values(self):
        for section in Configuration.SECTION:
            if not self.config_parser.has_section(section):
                self.config_parser.add_section(section)

        ''' Paths '''
        self.config_parser.set(Configuration.SECTION[0],
                               Configuration.OPT_DATA_PATH,
                               Configuration.DATA_PATH)
        self.config_parser.set(Configuration.SECTION[0],
                               Configuration.OPT_LOCALE_PATH,
                               Configuration.LOCALE_PATH)
        ''' Graphics'''
        self.config_parser.set(Configuration.SECTION[1],
                               Configuration.OPT_SCREEN_WIDTH,
                               Configuration.SCREEN_SIZE[0])
        self.config_parser.set(Configuration.SECTION[1],
                               Configuration.OPT_SCREEN_HEIGHT,
                               Configuration.SCREEN_SIZE[1])
        self.config_parser.set(Configuration.SECTION[1],
                               Configuration.OPT_FULLSCREEN,
                               Configuration.FULLSCREEN)
        ''' Sound '''
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
        ''' Control '''
        self.config_parser.set(Configuration.SECTION[3],
                               Configuration.OPT_CONTROL_TYPE,
                               Configuration.CONTROL_TYPE),
        self.config_parser.set(Configuration.SECTION[3],
                               Configuration.OPT_KEY_UP,
                               Configuration.KEY_UP),
        self.config_parser.set(Configuration.SECTION[3],
                               Configuration.OPT_KEY_DOWN,
                               Configuration.KEY_DOWN),
        self.config_parser.set(Configuration.SECTION[3],
                               Configuration.OPT_KEY_LEFT,
                               Configuration.KEY_LEFT),
        self.config_parser.set(Configuration.SECTION[3],
                               Configuration.OPT_KEY_RIGHT,
                               Configuration.KEY_RIGHT),
        self.config_parser.set(Configuration.SECTION[3],
                               Configuration.OPT_KEY_ACTION_1,
                               Configuration.KEY_ACTION_1),
        self.config_parser.set(Configuration.SECTION[3],
                               Configuration.OPT_KEY_ACTION_2,
                               Configuration.KEY_ACTION_2)
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
        self.control_type = Configuration.CONTROL_TYPE
        self.key_up = Configuration.KEY_UP
        self.key_down = Configuration.KEY_DOWN
        self.key_left = Configuration.KEY_LEFT
        self.key_right = Configuration.KEY_RIGHT
        self.key_act1 = Configuration.KEY_ACTION_1
        self.key_act2 = Configuration.KEY_ACTION_2

    def save(self):
        with open(Configuration.CFGFILE_NAME, 'wb') as config_file:
            self.config_parser.write(config_file)
