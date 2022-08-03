from os.path import exists, join

import yaml


class Config:
    def __init__(self):
        self.filename = ".config.yml"

        self.default_config = {"width": None, "height": None}
        self.dict = self.load()

    def load(self):
        if not exists(self.filename):
            with open(self.filename, "w") as f:
                yaml.safe_dump(self.default_config, f)

        with open(self.filename, "r") as f:
            return yaml.safe_load(f)

    def save(self):
        with open(self.filename, "w") as f:
            yaml.safe_dump(self.dict, f)
