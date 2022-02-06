"""utils module."""
import yaml
import datetime


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    def __getattr__(*args):
        _ = dict.get(*args)
        return DotDict(_) if type(_) is dict else _
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def configuration() -> dict:
    with open("/config.yml", "r") as _config_yml:
        config = yaml.load(_config_yml, Loader=yaml.FullLoader)
        return DotDict(config)


def get_delayed_time_to_start():
    now = datetime.datetime.now()
    start = now.replace(minute=50, second=00)

    if now.minute in range(50, 60):
        start += datetime.timedelta(hours=1)

    return start - now

def remove_command_from_message(msg: str):
    result = ""
    for m in msg.split(' ')[1:]:
        result += m + " "
    return result
