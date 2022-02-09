import asyncio
import datetime

from notion_client import AsyncClient

notion = AsyncClient(auth=ENV['NOTION_INTEGRATION_TOKEN'])


from pprint import pprint


PROPERTY_ID = {}
async def get_property_id():
    global PROPERTY_ID
    response = await notion.databases.retrieve(
        **{
            "database_id": ENV['DAILY_DATABASE'],
        }
    )

    for key, value in response['properties'].items():
        PROPERTY_ID[key] = value['id']



async def update_property(date: str):
    global PROPERTY_ID
    response = await notion.pages.update(
        **{
            "page_id": await get_page_id_with_date(date),
            "properties": {
                PROPERTY_ID['DOT2']: {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "hello world!"
                            }
                        }
                    ]
                }
            }
        }
    )
    pprint(response)

async def get_page_id_with_date(date: str):
    response = await notion.databases.query(
        **{
            "database_id": ENV['DAILY_DATABASE'],
            "filter": {
                "property": "CREATED TIME",
                "created_time": {
                    "equals": date
                }
            }
        }
    )
    # pprint(response)
    return response['results'][0]['id']

async def find_properties(_id: str, _time: int):
    global PROPERTY_ID
    response = await notion.pages.properties.retrieve(
        **{
            "page_id": _id,
            "property_id": PROPERTY_ID['DOT1']
        }
    )


async def get_page(date: str):
    _id = await get_page_id_with_date(date)

    await find_properties(_id, 0)



# asyncio.run(update_property("2022-01-24"))

async def main():
    await get_property_id()
    # await get_page('2022-01-24')
    await update_property('2022-01-24')

asyncio.run(main())