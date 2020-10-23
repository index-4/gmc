import os
import sys
import yaml
from yamlinclude import YamlIncludeConstructor

YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores its' path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Config:

    __instance = None
    content: dict = {}

    def __new__(cls):
        if Config.__instance is None:
            Config.__instance = object.__new__(cls)
        return Config.__instance

    def __init__(self):
        with open(resource_path('config.yaml'), "r") as config_file:
            self.content = yaml.load(config_file, Loader=yaml.FullLoader)

    def edit(self):
        os.system(f"{self.content['public_config']['default_editor']} public_config.yaml")
