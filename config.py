import os
import yaml


def get_keyword(key):
    if not os.path.exists('config.yml'):
        raise OSError('\'config.yaml\' does not exist!')

    with open('config.yml', 'r', encoding='utf-8') as yaml_file:
        data = yaml.load(yaml_file, Loader=yaml.FullLoader)

    if not data.get(key):
        raise KeyError('There is not {} field in config.yaml'.format(key))

    return data[key]