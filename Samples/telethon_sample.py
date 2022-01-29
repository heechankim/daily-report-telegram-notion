
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
    with open("config.yml", "r") as _config_yml:
        config = yaml.load(_config_yml, Loader=yaml.FullLoader)
        return DotDict(config)


from telethon.sync import TelegramClient, events

config = configuration()


BOT = config.telegram.bot.name

client = TelegramClient(
    config.telegram.me.name,
    config.telegram.me.api.id,
    config.telegram.me.api.hash
)


@client.on(events.NewMessage(chats=BOT))
async def get_message_from_bot(event):
    if event.sender_id == int(config.telegram.bot.id):
        print("From bot : " + event.raw_text)
    else:
        print("From " + str(event.sender_id) + " : " + event.raw_text)

client.start()
client.connect()
client.send_message(BOT, "/start")

client.run_until_disconnected()