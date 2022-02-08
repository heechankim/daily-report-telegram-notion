from telegram.ext import CallbackContext
from telegram import Update

from DailyReport.databases.notion_database import NotionDatabase

from DailyReport.utils.utils import remove_command_from_message
from DailyReport.utils.Either import Either, Left, Right


def EitherHandler(either: Either, update: Update, context: CallbackContext):
    if isinstance(either, Right):
        context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=either.context['result']
        )
    else:
        context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=either.context['message']
        )


class Commands:
    def __init__(
            self,
            chat_id: int,
            notion: NotionDatabase
    ):
        self.chat_id = chat_id
        self.notion = notion

    def start(self, update: Update, context: CallbackContext):
        msg = remove_command_from_message(update.message.text)

        either = self.notion.new_user({
            "telegram_id": update.message.from_user.id,
        })

        EitherHandler(either, update, context)

    def setRoot(self, update: Update, context: CallbackContext):
        msg = remove_command_from_message(update.message.text)

        either = self.notion.set_user_root({
            "telegram_id": update.message.from_user.id,
            "root": msg
        })

        EitherHandler(either, update, context)

    def setToken(self, update: Update, context: CallbackContext):
        msg = remove_command_from_message(update.message.text)

        either = self.notion.set_user_token({
            "telegram_id": update.message.from_user.id,
            "integration_token": msg
        })

        EitherHandler(either, update, context)

    def rp(self, update: Update, context: CallbackContext):
        msg = remove_command_from_message(update.message.text)

        either = self.notion.report({
            "telegram_id": update.message.from_user.id,
            "message": msg,
            "datetime": update.message.date
        })

        EitherHandler(either, update, context)

    def todo(self, update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=self.chat_id,
            text="Testing todo Command."
        )

        """
        {'update_id': 208513719, 'message': {'new_chat_members': [], 'supergroup_chat_created': False, 'channel_chat_created': False, 'photo': [], 'text': '/rp hello 123 ""aa 1 :: 12 : 😂', 'delete_chat_photo': False, 'caption_entities': [], 'entities': [{'type': 'bot_command', 'offset': 0, 'length': 3}], 'message_id': 634, 'new_chat_photo': [], 'date': 1644130630, 'chat': {'type': 'private', 'last_name': '김', 'first_name': '희찬', 'id': 2084891827, 'username': 'heechan_kim'}, 'group_chat_created': False, 'from': {'language_code': 'ko', 'last_name': '김', 'is_bot': False, 'first_name': '희찬', 'username': 'heechan_kim', 'id': 2084891827}}}
        """

        """
        시나리오 :
        /start
        /setToken
        /setRoot
        /begin
        """