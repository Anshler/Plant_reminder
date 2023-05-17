# set configuration e.g: theme

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources
import yaml

meta_config = yaml.safe_load(open(resources.path('app_config','meta_config.yaml'),encoding='utf-8'))
theme_list = yaml.safe_load(open(resources.path('app_config','theme.yaml'),encoding='utf-8'))

theme = meta_config['theme']
language = meta_config['language']