# https://stackoverflow.com/a/1305682/6719849
class Dict2Class(object):
    def __init__(self, d):
        for k, v in d.items():
            setattr(self, k, v)
