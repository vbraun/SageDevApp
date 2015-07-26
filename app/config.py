
import logging
log = logging.getLogger()

import os
import yaml
from copy import deepcopy
import pprint



class Configuration(object):
    
    def __init__(self, entries):
        self._dict = deepcopy(entries)
        self.__dict__.update(entries)

    def _format(self, indent):
        for key in sorted(self._dict.keys()):
            value = self._dict[key]
            if isinstance(value, Configuration):
                yield ' '*indent + key + ':'
                yield from value._format(indent+4)
            else:
                yield ' '*indent + key + ': ' + str(value)
        
    def __repr__(self):
        return '\n'.join(self._format(4))



class ConfigurationFactory(object):

    def merge_dictionaries(self, *dictionaries):
        assert dictionaries, 'must pass at least one value'
        if not any(isinstance(d, dict) for d in dictionaries):
            return dictionaries[0]
        elif all(isinstance(d, dict) for d in dictionaries):
            keys = set()
            for d in dictionaries:
                keys.update(d.keys())
            result = dict()
            for k in keys:
                values = [d[k] for d in dictionaries if k in d]
                result[k] = self.merge_dictionaries(*values)
            return result
        else:
            raise ValueError('cannot merge dictionary with non-dictionary: {0}'.format(dictionaries))
        
    def dict_to_configuration(self, *args):
        dictionary = self.merge_dictionaries(*args)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                dictionary[key] = self.dict_to_configuration(value)
        return Configuration(dictionary)

    def load_app_yaml(self):
        APP_YAML = os.path.join(
            os.path.dirname(__file__), '..', 'app.yaml')
        with open(APP_YAML, 'rb') as f:
            return yaml.load(f)
            
    def load_app_default_yaml(self):
        APP_DEFAULT_YAML = os.path.join(
            os.path.dirname(__file__), '..', 'app-default.yaml')
        with open(APP_DEFAULT_YAML, 'rb') as f:
            return yaml.load(f)

    def load(self):
        APP_YAML = self.load_app_yaml()
        APP_DEFAULT_YAML = self.load_app_default_yaml()
        return self.dict_to_configuration(APP_YAML, APP_DEFAULT_YAML)



config = ConfigurationFactory().load()

# print(config)

