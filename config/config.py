# -*- coding:utf-8 -*-
from configparser import RawConfigParser
import os
config = RawConfigParser()
config_path = os.path.split(os.path.realpath(__file__))[0] + '/config.conf'
config.read(config_path)
if __name__ == '__main__':
    print(config_path)
    print(config.get('database', 'dict'))

