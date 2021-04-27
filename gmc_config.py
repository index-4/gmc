import os
import sys
import yaml
import appdirs
from shutil import copy2


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
        with open(resource_path("config.yaml"), "r") as config_file:
            self.content = yaml.safe_load(config_file)

            if not os.path.exists(
                appdirs.user_config_dir("gmc", "index4")
            ):
                # save config locally if is non existent
                os.makedirs(appdirs.user_config_dir("gmc", "index4"))
                copy2(
                    resource_path("public_config.yaml"),
                    appdirs.user_config_dir("gmc", "index4"),
                )
            for to_include in self.content["includes"]:
                with open(
                    f"{appdirs.user_config_dir('gmc', 'index4')}/{to_include}",
                    "r",
                ) as local_config_file:
                    self.content.update(
                        {
                            to_include.replace(".yaml", ""): yaml.safe_load(
                                local_config_file
                            )
                        }
                    )

    def edit(self):
        os.system(
            f"{self.content['public_config']['default_editor']} {appdirs.user_config_dir('gmc', 'index4')}/public_config.yaml"
        )
