import asyncio
from pprint import pprint
import logging
from dataclasses import dataclass

from notion_client import AsyncClient
from notion_client import APIResponseError, APIErrorCode

from DailyReport.utils import configuration
config = configuration("./config.yml").notion


@dataclass
class Response:
    result: bool
    response: dict = None
    code: APIErrorCode = None


class NotionAPIs:
    def __init__(
            self,
            token: str
    ):
        self.notion = AsyncClient(auth=token)
        self.log = logging.getLogger("[CLASS_APIS]")

    def if_error_return_code(function):
        async def wrapper(*args, **kwargs):
            self = args[0]
            try:
                return await function(*args, **kwargs)
            except Exception as e:
                return Response(result=False, code=APIErrorCode(e.code))
        return wrapper

    async def close(self):
        await self.notion.aclose()

    async def init_app_page(self, root: str):
        await self.init_sub_update_page_title(root)

    @if_error_return_code
    async def init_sub_update_page_title(self, root):
        response = await self.notion.pages.update(
            **{
                "page_id": root,
                "icon": {
                    "external": {
                        "url": "https://img.icons8.com/ios/250/000000/database.png"
                    },
                },
                "properties": {
                    'title': {
                        "title": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "app database"
                                }
                            }
                        ],
                    }
                },
            }
        )

        return Response(result=True, response=response)

    async def init_sub_create_daily_page(self, context):
        ...


async def main():
    notion = NotionAPIs(config.integration)

    await notion.init_app_page(config.pages.root)

    await notion.close()


if __name__ == "__main__":
    asyncio.run(main())
