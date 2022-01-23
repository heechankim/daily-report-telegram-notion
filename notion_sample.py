from dotenv import dotenv_values
CHAN = dotenv_values(".env")

from notion_client import Client

notion = Client(auth=CHAN['NOTION_INTEGRATION_TOKEN'])

from pprint import pprint


my_page = notion.databases.query(
    **{
        "database_id": CHAN['DR_ID'],
    }
)
pprint(my_page)