from notion_client import AsyncClient
from DailyReport.utils.utils import configuration

import asyncio

EMPTY_PAGE = "e7f3fde5ab364696aba5434dfa6eff5e"

config = configuration()
notion = AsyncClient(auth=config.notion.integration.token)


async def app_page_init(page_id: str):
    response = await notion.pages.update(
        **{
            "page_id": page_id,
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
                                 "content": "app database(rename your self)"
                             }
                         }
                    ],
                }
            },
        }
    )



async def main():
    await app_page_init(EMPTY_PAGE)


if __name__ == "__main__":
    asyncio.run(main())
