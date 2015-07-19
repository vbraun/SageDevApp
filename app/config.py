
import logging
log = logging.getLogger()

import os
import yaml




class Configuration:
    def __init__(self, entries): 
        self.__dict__.update(entries)
        

APP_YAML = os.path.join(
    os.path.dirname(__file__), '..', 'app.yaml')

with open(APP_YAML, 'rb') as f:
    config = Configuration(yaml.load(f))

