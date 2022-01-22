import time

from dotenv import dotenv_values
CHAN = dotenv_values(".env")

from telethon import TelegramClient, events, sync

BOT = "chan_report_bot"
client = TelegramClient('chan', CHAN['API_ID'], CHAN['API_HASH'])


@client.on(events.NewMessage(chats=BOT))
async def get_message_from_bot(event):
    if event.sender_id == int(CHAN['BOT_ID']):
        print("From bot : " + event.raw_text)
    else:
        print("From " + str(event.sender_id) + " : " + event.raw_text)

client.start()
client.connect()
client.send_message(BOT, "/start")

client.run_until_disconnected()