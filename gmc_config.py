import os
import sys
import yaml

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores its' path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.realpath(__file__))

    return os.path.join(base_path, relative_path)


class Config:

    content: dict = {}

    def __init__(self):
        with open(resource_path('config.yaml'), "r") as config_file:
            self.content = yaml.safe_load(config_file)
            for to_include in self.content["includes"]:
                with open(resource_path(to_include)) as include_file:
                    self.content.update({to_include.replace(".yaml", ""): yaml.safe_load(include_file)})

    def edit(self):
        os.system(f"{self.content['public_config']['default_editor']} {resource_path('public_config.yaml')}")
