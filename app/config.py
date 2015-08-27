
import logging
log = logging.getLogger()

import os
import yaml
from copy import deepcopy
import pprint
import collections


class Configuration(collections.UserDict):
    
    def __init__(self, entries):
        super().__init__(entries)

    def __getattr__(self, key):
        try:
            return self.__dict__['data'][key]
        except KeyError:
            raise AttributeError(key)

    def _format(self, indent):
        for key in sorted(self.data.keys()):
            value = self.data[key]
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

    def expand_templates(self, config, format_kwds):
        """
        Expand Python string format in dictionary values
        """
        for key, value in config.data.items():
            if isinstance(value, Configuration):
                self.expand_templates(value, format_kwds)
            elif isinstance(value, str):
                config.data[key] = value.format(**format_kwds)
            else:
                pass
        return config
        
    def load_app_yaml(self):
        APP_YAML = os.path.join(
            os.path.dirname(__file__), '..', 'app.yaml')
        if not os.path.exists(APP_YAML):
            log.info('Configuration file not found: {0}'.format(APP_YAML))
            return dict()
        with open(APP_YAML, 'rb') as f:
            return yaml.load(f)
            
    def load_app_default_yaml(self):
        APP_DEFAULT_YAML = os.path.join(
            os.path.dirname(__file__), '..', 'app-default.yaml')
        if not os.path.exists(APP_DEFAULT_YAML):
            log.info('Configuration file not found: {0}'.format(APP_DEFAULT_YAML))
            return dict()
        with open(APP_DEFAULT_YAML, 'rb') as f:
            return yaml.load(f)

    def repo_root(self):
        return os.path.dirname(os.path.dirname(__file__))
        
    def load(self):
        APP_YAML = self.load_app_yaml()
        APP_DEFAULT_YAML = self.load_app_default_yaml()
        config = self.dict_to_configuration(APP_YAML, APP_DEFAULT_YAML)
        if not os.path.isabs(config.data_files.prefix):
            config.data_files.data['prefix'] = os.path.join(
                self.repo_root(),
                config.data_files.prefix
            )
        return self.expand_templates(config, format_kwds=deepcopy(config.data))



config = ConfigurationFactory().load()


print('Configuration:')
print(config)

