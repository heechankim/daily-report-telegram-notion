import typer
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone

# telegram
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler

# env
from dotenv import dotenv_values
CHAN = dotenv_values(".env")


app = typer.Typer()
updater = None
dispatcher = None
sch = None


def bot_start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=CHAN['CHAT_ID'], text="I'm a bot, please talk to me!")


start_handler = CommandHandler('start', bot_start)


@app.command()
def start():
    global sch
    global updater
    global dispatcher
    #typer.echo(f"Hello {name}")
    updater = Updater(token=CHAN['TOKEN'], use_context=True)
    dispatcher = updater.dispatcher

    sch = BackgroundScheduler()
    sch.configure(timezone=timezone('Asia/Seoul'))
    sch.start()
    sch.add_job(updater.start_polling)


@app.command()
def end():
    global sch
    global updater
    updater.stop()
    sch.shutdown()

@app.command()
def watch(end: bool = False):
    global dispatcher
    global start_handler
    if end:
        dispatcher.remove_handler(start_handler)
    else:
        dispatcher.add_handler(start_handler)


if __name__ == "__main__":
    app()