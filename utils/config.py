try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources
import yaml

meta_config = yaml.safe_load(open(resources.path('config','meta_config.yaml'),encoding='utf-8'))
config = yaml.safe_load(open(resources.path('config','config_list.yaml'),encoding='utf-8'))

primary_font_color= config['theme'][meta_config['theme']]['primary_font_color']
secondary_font_color= config['theme'][meta_config['theme']]['secondary_font_color']
background_color = config['theme'][meta_config['theme']]['background_color']
wrong_pass_warn = config['theme'][meta_config['theme']]['wrong_pass_warn']
press_word_button = config['theme'][meta_config['theme']]['press_word_button']