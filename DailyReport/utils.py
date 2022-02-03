"""utils module."""
import yaml


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    def __getattr__(*args):
        _ = dict.get(*args)
        return DotDict(_) if type(_) is dict else _
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def configuration() -> dict:
    with open("/Users/chan/PycharmProjects/daily-report-telegram-notion/config.yml", "r") as _config_yml:
        config = yaml.load(_config_yml, Loader=yaml.FullLoader)
        return DotDict(config)
