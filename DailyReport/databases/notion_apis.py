import asyncio
from pprint import pprint
import logging
from dataclasses import dataclass
import datetime

from notion_client import AsyncClient
from notion_client import APIResponseError, APIErrorCode

from DailyReport.entities import RichText
from DailyReport.utils import configuration
config = configuration("./config.yml").notion


@dataclass
class Response:
    result: bool
    response: dict = None
    code: APIErrorCode = None
    message: str = ""


class NotionAPIs:
    def __init__(
            self,
            token: str
    ):
        self.notion = AsyncClient(auth=token)
        self.log = logging.getLogger("[CLASS_APIS]")
        self.daily_prop_ids = {}

    async def close(self):
        await self.notion.aclose()

    def if_error_return_code(function):
        async def wrapper(*args, **kwargs):
            self = args[0]
            try:
                return await function(*args, **kwargs)
            except Exception as e:
                return Response(
                    result=False,
                    code=APIErrorCode(e.code),
                    message=e.args
                )
        return wrapper

    def generate_database_prop(self):
        p = dict()

        hours = range(1, 25)
        for h in hours:
            p[str(h) + "oclock"] = {
                "rich_text": []
            }
        p['Name'] = {"title": {}}
        p['CREATED TIME'] = {"created_time": {}}

        return p

    async def init_app_page(self, root: str):
        await self.update_app_page_title(root)

        res = await self.create_daily_report_page(root)

        self.init_daily_report_properties_id(res.response['id'])

        return res.response['id']

        # return res.response

    @if_error_return_code
    async def update_app_page_title(self, root):
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

    @if_error_return_code
    async def create_daily_report_page(self, root):
        response = await self.notion.databases.create(
            **{
                "parent": {
                    "type": "page_id",
                    "page_id": root,
                },
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": "DailyReport"
                        }
                    }
                ],
                "properties": self.generate_database_prop()
            }
        )

        return Response(result=True, response=response)

    @if_error_return_code
    async def init_daily_report_properties_id(self, daily):
        response = await self.notion.databases.retrieve(
            **{
                "database_id": daily
            }
        )

        for key, value in response['properties'].items():
            self.daily_prop_ids[key] = value['id']

    @if_error_return_code
    async def get_page_id_by_date_in_daily_report(self, daily, date):
        response = await self.notion.databases.query(
            **{
                "database_id": daily,
                "filter": {
                    "property": "CREATED TIME",
                    "created_time": {
                        "equals": date
                    }
                }
            }
        )

        if not response['results']:
            return Response(result=False, message="Page isn't exist.")

        return Response(result=True, response=response['results'][0]['id'])

    @if_error_return_code
    async def is_today_page_exist(self, daily):
        result = await self.get_page_id_by_date_in_daily_report(daily, datetime.date.today().isoformat())

        return result

    @if_error_return_code
    async def create_today_page_in_daily_report(self, daily):
        result = await self.is_today_page_exist(daily)

        if result.result:
            return Response(result=False)

        response = await self.notion.pages.create(
            **{
                "parent": {
                    "database_id": daily
                },
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": datetime.date.today().isoformat()
                                }
                            }
                        ]
                    }
                }
            }
        )

        return Response(result=True, response=response)

    @if_error_return_code
    async def retrieve_page_property(self, page: str, oclock: int):

        _oclock = str(oclock) + "oclock"

        response = await self.notion.pages.properties.retrieve(
            **{
                "page_id": page,
                "property_id": self.daily_prop_ids[_oclock]
            }
        )

        if not response['results']:
            return Response(result=False, message="Property isn't exist.")

        r = RichText(**response['results'][0])

        return Response(result=True, response=r)


    @if_error_return_code
    async def update_today_page_property(self, daily: str, oclock: int, text: str):
        today_page = await self.get_page_id_by_date_in_daily_report(daily, datetime.date.today().isoformat())
        today_page_id = today_page.response

        _oclock = str(oclock) + "oclock"
        _text = ""

        p = await self.retrieve_page_property(today_page_id, oclock)
        if p.result:
            _text += p.response.rich_text.text.content
            _text += " / "

        _text += text

        response = await self.notion.pages.update(
            **{
                "page_id": today_page_id,
                "properties": {
                    _oclock: {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": _text
                                }
                            }
                        ]
                    }
                }
            }
        )

        return Response(result=True, response=response)


async def main():
    notion = NotionAPIs(config.integration)

    # result_id = await notion.init_app_page(config.pages.root)

    # result = await notion.create_today_page_in_daily_report(config.pages.daily)

    # result = await notion.get_page_id_by_date_in_daily_report(
    #     config.pages.daily,
    #     datetime.date.today().isoformat()
    # )

    # result = await notion.update_today_page_property(
    #     config.pages.daily,
    #     19,
    #     "test !!!!"
    # )

    await notion.init_daily_report_properties_id(
        config.pages.daily
    )
    today = await notion.get_page_id_by_date_in_daily_report(
        config.pages.daily,
        datetime.date.today().isoformat()
    )

    result = await notion.update_today_page_property(
        config.pages.daily,
        19,
        "hello world!!!!!"
    )

    pprint(result)

    await notion.close()


if __name__ == "__main__":
    asyncio.run(main())
