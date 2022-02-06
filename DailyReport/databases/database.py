from tinydb import TinyDB, where
import pathlib


FILE = pathlib.Path(__file__)
DIR = FILE.parent
DB = DIR / "db.json"

"""
return type
{
    "failed": True | False,
    "result": "error message" | "success value"
}
"""


class Database:
    def __init__(self):
        self.path = DB

    def init_user(self, telegram_id: int, root_page_id: str):
        if self.is_user(telegram_id)['failed'] is False:
            return

        with TinyDB(self.path) as db:
            users = db.table("users")
            users.insert({
                "id": telegram_id,
                "pages": {
                    "root": root_page_id,
                    "daily": "",
                }
            })
            return {"failed": False, "result": "failed"}

    def is_user(self, telegram_id: int):
        with TinyDB(self.path) as db:
            result = db.table("users").get(where('id') == telegram_id)

            if result is None:
                return {"failed": True, "result": "\'/start page_id\' 로 페이지 추가 필요."}

            return {"failed": False, "result": result['pages']['root']}



