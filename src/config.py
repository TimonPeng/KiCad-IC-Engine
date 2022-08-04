from copy import deepcopy
from os.path import exists, join

import yaml


# https://stackoverflow.com/a/1305682/6719849
class Config:
    def __init__(self):
        self.filename = ".config.yml"

        self.default_config = {"width": None, "height": None}
        self.load()

    def set_attr(self, config):
        for k, v in config.items():
            setattr(self, k, v)

    def load(self):
        # if config not exists, create it with default values
        if not exists(self.filename):
            self.save()

        with open(self.filename, "r") as f:
            config = yaml.safe_load(f) or {}

            # merge config with default values
            self.set_attr(self.default_config | config)

    def save(self):
        with open(self.filename, "w") as f:
            config = deepcopy(self.__dict__)

            for key in ["filename", "default_config"]:
                config.pop(key)

            yaml.safe_dump(config, f)
