from pathlib import PurePath
from os.path import join
import configparser


class ConfigurationHandler:
    def __init__(self, abs_instance_path):
        self.CONFIG_DIR = 'cfg'
        self.CONFIG_FILENAME = self.instance_name_from(abs_instance_path)
        self.CONFIG_FORMAT = '.config'

    @staticmethod
    def instance_name_from(abs_instance_path):
        return PurePath(abs_instance_path).stem

    def read_section_by(self, name):
        config = configparser.ConfigParser()
        config.read(join(self.CONFIG_DIR, f'{self.CONFIG_FILENAME}{self.CONFIG_FORMAT}'))
        section = config[name]
        return section
