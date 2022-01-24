import asyncio
import datetime

from dotenv import dotenv_values
ENV = dotenv_values(".env")

from notion_client import AsyncClient

notion = AsyncClient(auth=ENV['NOTION_INTEGRATION_TOKEN'])



from pprint import pprint

async def new_page_in_database():
    response = await notion.pages.create(
        **{
            "parent": {
                "type": "database_id",
                "database_id": ENV['DR_ID'],
            },
            "properties": {
                "Name": {
                    "title": [{
                        "text": {
                            "content": 'test'
                        }
                    }]
                },
            },
            "children": [
                {
                    "object": 'block',
                    "type": 'heading_2',
                    "heading_2": {
                        "text": [
                            {
                                "type": 'text',
                                "text": {
                                    "content": 'Lacinato kale',
                                },
                            },
                        ],
                    },
                },
            ]
        }
    )
    pprint("new page created \n")
    pprint(response)
    return response['id']

async def get_page_retrieve():
    response = await notion.pages.retrieve(
        **{
            "page_id": "e4398a85-55fa-44ef-9e08-951af8aa683d"
        }
    )
    pprint(response)
    return response

async def get_page_contents():
    response = await notion.blocks.children.list(
        **{
            "block_id": "0391b46b309e42de866b9efe026878f8",
            "page_size": 100,
        }
    )
    return response['results']


async def get_dr_table():
    page = await get_page_contents()

    # 해당 페이지에서 table 블록의 id를 찾는다.
    for item in page:
        if item['type'] == "table":
            _table = item

    table = await notion.blocks.children.list(
        **{
            "block_id": _table['id']
        }
    )
    table = table['results']

    # 테이블에서 시간으로 검색하여 id 얻기
    for item in table:
        # pprint(item['table_row']['cells'][0][0]['plain_text'])
        if item['table_row']['cells'][0][0]['plain_text'] == "24":
            _row = item

    inputText = "testtttt"
    new_table_row = _row['table_row']
    # new_table_row['cells'][1] = [{
    #     'type': 'text',
    #     'text': {'content': inputText,
    #              'link': None},
    #     'annotations': {'bold': False,
    #                     'italic': False,
    #                     'strikethrough': False,
    #                     'underline': False,
    #                     'code': False,
    #                     'color': 'default'},
    #     'plain_text': inputText,
    #     'href': None
    # }]
    # new_table_row['cells'][1] = [{
    #     'type': 'text',
    #     'text': {
    #         'content': inputText,
    #     },
    # }]
    new_table_row = {
        'cells': [[], [{
            'type': 'text',
            'text': {
                'content': "testtttt"
            }
        }], []]
    }

    # pprint(_row)
    # pprint("======")
    # pprint({
    #         "block_id": _row['id'],
    #         "table_row": new_table_row,
    #     })


    response = await notion.blocks.update(
        **{
            "block_id": _row['id'],
            "table_row": new_table_row,
        }
    )
    pprint(response)


async def get_database():
    response = await notion.databases.retrieve(ENV['DR_ID'])
    pprint(response)


async def get_page_with_date_in_database(date: str):
    response = await notion.databases.query(
        **{
            "database_id": ENV['DR_ID'],
            "filter": {
                "property": "CREATED TIME",
                "created_time": {
                    "equals": date
                }
            }
        }
    )
    pprint(response)


async def get_page():
    response = await notion.pages.retrieve(
        **{
            "page_id": await new_page_in_database()
        }
    )

async def update_page():
    response = await notion.pages.update(
        **{
            "page_id": "80bc9d6840a840d1b9a7d3d95adc68f8",
            "children": [
                {
                    "object": 'block',
                    "type": 'heading_2',
                    "heading_2": {
                        "text": [
                            {
                                "type": 'text',
                                "text": {
                                    "content": 'Lacinato kale',
                                },
                            },
                        ],
                    },
                },
            ]
        }
    )
    pprint(response)

# asyncio.run(get_page_with_date_in_database("2022-01-24"))
# asyncio.run(new_page_in_database())
asyncio.run(get_database())

