from gettext import gettext as _
import os
import ConfigParser


class ConfigurationError(Exception):
    def __init__(self, value):
        super(ConfigurationError, self).__init__()
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
    OPT_KEY_START = 'key start'

    ''' Default values '''
    DATA_PATH = './'
    LOCALE_PATH = 'locale'
    SECTION = ['Paths', 'Graphics', 'Sound', 'Control']
    SCREEN_SIZE = [1024, 768]
    FULLSCREEN = False
    SOUND = True
    MUSIC = True
    SOUND_VOLUME = 5
    MUSIC_VOLUME = 5
    CFGFILE_NAME = 'solstice.cfg'
    CONTROL_TYPE = 'autodetect'
    KEY_UP = 119
    KEY_DOWN = 115
    KEY_LEFT = 97
    KEY_RIGHT = 100
    KEY_ACTION_1 = 117
    KEY_ACTION_2 = 105
    KEY_START = 13

    def __init__(self):
        self.parser = ConfigParser.ConfigParser()

        try:
            parsed_file = self.parser.read([Configuration.CFGFILE_NAME])

            if len(parsed_file) > 0:
                self.data_path = self.parser.get(
                    Configuration.SECTION[0], Configuration.OPT_DATA_PATH)
                self.__check_correct_values(
                    Configuration.OPT_DATA_PATH, self.data_path)
                self.locale_path = self.parser.get(
                    Configuration.SECTION[0], Configuration.OPT_LOCALE_PATH)
                w = self.parser.getint(Configuration.SECTION[1],
                                       Configuration.OPT_SCREEN_WIDTH)
                self.__check_correct_values(Configuration.OPT_SCREEN_WIDTH, w)
                h = self.parser.getint(Configuration.SECTION[1],
                                       Configuration.OPT_SCREEN_HEIGHT)
                self.__check_correct_values(Configuration.OPT_SCREEN_HEIGHT, h)
                self.fullscreen = self.parser.getboolean(
                    Configuration.SECTION[1], Configuration.OPT_FULLSCREEN)
                self.sound = self.parser.getboolean(
                    Configuration.SECTION[2], Configuration.OPT_SOUND)
                self.music = self.parser.getboolean(
                    Configuration.SECTION[2], Configuration.OPT_MUSIC)
                self.sound_vol = self.parser.getint(
                    Configuration.SECTION[2], Configuration.OPT_SOUND_VOL)
                self.__check_correct_values(
                    Configuration.OPT_SOUND_VOL, self.sound_vol)
                self.music_vol = self.parser.getint(
                    Configuration.SECTION[2], Configuration.OPT_MUSIC_VOL)
                self.__check_correct_values(
                    Configuration.OPT_MUSIC_VOL, self.music_vol)
                self.screen_size = (w, h)
                self.control_type = self.parser.get(
                    Configuration.SECTION[3], Configuration.OPT_CONTROL_TYPE)
                self.__check_correct_values(
                    Configuration.OPT_CONTROL_TYPE, self.control_type)
                self.key_up = self.parser.getint(
                    Configuration.SECTION[3], Configuration.OPT_KEY_UP)
                self.key_down = self.parser.getint(
                    Configuration.SECTION[3], Configuration.OPT_KEY_DOWN)
                self.key_left = self.parser.getint(
                    Configuration.SECTION[3], Configuration.OPT_KEY_LEFT)
                self.key_right = self.parser.getint(
                    Configuration.SECTION[3], Configuration.OPT_KEY_RIGHT)
                self.key_act1 = self.parser.getint(
                    Configuration.SECTION[3], Configuration.OPT_KEY_ACTION_1)
                self.key_act2 = self.parser.getint(
                    Configuration.SECTION[3], Configuration.OPT_KEY_ACTION_2)
                self.key_start = self.parser.getint(
                    Configuration.SECTION[3], Configuration.OPT_KEY_START)
            else:
                self.__set_default_values()

        except ConfigurationError as e:
            print(e.value)
            self.__set_default_values()
        except:
            self.__set_default_values()

    def __set_default_values(self):
        for section in Configuration.SECTION:
            if not self.parser.has_section(section):
                self.parser.add_section(section)

        ''' Paths '''
        self.parser.set(Configuration.SECTION[0],
                        Configuration.OPT_DATA_PATH,
                        Configuration.DATA_PATH)
        self.parser.set(Configuration.SECTION[0],
                        Configuration.OPT_LOCALE_PATH,
                        Configuration.LOCALE_PATH)
        ''' Graphics'''
        self.parser.set(Configuration.SECTION[1],
                        Configuration.OPT_SCREEN_WIDTH,
                        Configuration.SCREEN_SIZE[0])
        self.parser.set(Configuration.SECTION[1],
                        Configuration.OPT_SCREEN_HEIGHT,
                        Configuration.SCREEN_SIZE[1])
        self.parser.set(Configuration.SECTION[1],
                        Configuration.OPT_FULLSCREEN,
                        Configuration.FULLSCREEN)
        ''' Sound '''
        self.parser.set(Configuration.SECTION[2],
                        Configuration.OPT_SOUND,
                        Configuration.SOUND)
        self.parser.set(Configuration.SECTION[2],
                        Configuration.OPT_MUSIC,
                        Configuration.MUSIC)
        self.parser.set(Configuration.SECTION[2],
                        Configuration.OPT_SOUND_VOL,
                        Configuration.SOUND_VOLUME)
        self.parser.set(Configuration.SECTION[2],
                        Configuration.OPT_MUSIC_VOL,
                        Configuration.MUSIC_VOLUME)
        ''' Control '''
        self.parser.set(Configuration.SECTION[3],
                        Configuration.OPT_CONTROL_TYPE,
                        Configuration.CONTROL_TYPE),
        self.parser.set(Configuration.SECTION[3],
                        Configuration.OPT_KEY_UP,
                        Configuration.KEY_UP),
        self.parser.set(Configuration.SECTION[3],
                        Configuration.OPT_KEY_DOWN,
                        Configuration.KEY_DOWN),
        self.parser.set(Configuration.SECTION[3],
                        Configuration.OPT_KEY_LEFT,
                        Configuration.KEY_LEFT),
        self.parser.set(Configuration.SECTION[3],
                        Configuration.OPT_KEY_RIGHT,
                        Configuration.KEY_RIGHT),
        self.parser.set(Configuration.SECTION[3],
                        Configuration.OPT_KEY_ACTION_1,
                        Configuration.KEY_ACTION_1),
        self.parser.set(Configuration.SECTION[3],
                        Configuration.OPT_KEY_ACTION_2,
                        Configuration.KEY_ACTION_2)
        self.parser.set(Configuration.SECTION[3],
                        Configuration.OPT_KEY_START,
                        Configuration.KEY_START)
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
        self.key_start = Configuration.KEY_START

    @staticmethod
    def __check_correct_values(option, read_value):

        if option == Configuration.OPT_DATA_PATH:
            file_path = ''.join([read_value, 'data.zip'])
            if not os.path.isfile(file_path):
                raise ConfigurationError(
                    _('Unable to find the data file in the directory specified in the configuration file.'))
        elif option == Configuration.OPT_SOUND_VOL:
            if read_value not in list(xrange(Configuration.SOUND_VOLUME + 1)):
                raise ConfigurationError(_('Sound volume must be between 0 (min) and 5 (max).'))
        elif option == Configuration.OPT_MUSIC_VOL:
            if read_value not in list(xrange(Configuration.MUSIC_VOLUME + 1)):
                raise ConfigurationError(_('Music volume must be between 0 (min) and 5 (max).'))
        elif option == Configuration.OPT_CONTROL_TYPE:
            if read_value not in ['keyboard', 'joystick', 'autodetect']:
                raise ConfigurationError(_('Control must be keyboard, joystick or autodetect.'))
        elif option == Configuration.OPT_SCREEN_WIDTH:
            if read_value < 1:
                raise ConfigurationError(_('Screen width must be between 1 and 1440.'))
        elif option == Configuration.OPT_SCREEN_HEIGHT:
            if read_value < 1:
                raise ConfigurationError(_('Screen height must be between 1 and 900.'))

    def save(self):
        with open(Configuration.CFGFILE_NAME, 'wb') as config_file:
            self.parser.write(config_file)
