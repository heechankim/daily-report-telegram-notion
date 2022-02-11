import logging
import asyncio

from aiogram import types

from DailyReport.databases import NotionDatabase
from DailyReport.utils import Either, Left, Right
from DailyReport.utils import remove_command_from_message

logger = logging.getLogger(__name__)


async def EitherHandler(either: Either, message: types.Message):
    if isinstance(either, Right):
        await message.answer(either.context['message'])
    else:
        await message.answer(either.context['message'])

class Commands:
    def __init__(
            self,
            notion: NotionDatabase
    ):
        self.notion = notion

    async def start(self, message: types.Message):
        either = self.notion.new_user({
            "telegram_id": message.chat.id,
        })

        await EitherHandler(either, message)

    async def setRoot(self, message: types.Message):
        msg = remove_command_from_message(message.text)

        either = self.notion.set_user_info({
            "telegram_id": message.chat.id,
            "root": msg
        })

        await EitherHandler(either, message)

    async def setNotion(self, message: types.Message):
        msg = remove_command_from_message(message.text)

        either = self.notion.set_user_info({
            "telegram_id": message.chat.id,
            "integration": msg
        })

        await EitherHandler(either, message)

    async def begin(self, message: types.Message):
        either = await self.notion.init_user_root_notion_page({
            "telegram_id": message.chat.id
        })

        await EitherHandler(either, message)

    async def rp(self, message: types.Message):
        msg = remove_command_from_message(message.text)

        either = await self.notion.report({
            "telegram_id": message.chat.id,
            "message": msg,
            "datetime": message.date
        })

        await EitherHandler(either, message)

    # def todo(self, update: Update, context: CallbackContext):
    #     context.bot.send_message(
    #         chat_id=self.chat_id,
    #         text="Testing todo Command."
    #     )

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