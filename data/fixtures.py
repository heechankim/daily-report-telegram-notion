from tinydb import TinyDB, Query, where
import pathlib

FILE = pathlib.Path(__file__)
DIR = FILE.parent
DB = DIR / "db.json"


def init_user(path):
    with TinyDB(path) as db:
        db.drop_table("users")
        user = db.table("users")
        user.insert({
            "id": 2084891827,
            "pages": {
                "root": "e7f3fde5ab364696aba5434dfa6eff5e",
                "daily": "",
            }
        })


def search_user(path):
    with TinyDB(path) as db:
        users = db.table('users')
        # result = users.search(where('id') == 2084891827)
        result = users.get(where('id') == 2084891821)

        if result is None:
            print("데이터 없음")



def create_tinydb(path):
    with TinyDB(path) as db:
        db.drop_table("routines")
        rt = db.table("routines")
        rt.insert({
            "job": {
                "name": "reporting what did"
            },
            "repeat": {
                "each": "day",
                "every": "hour",
                "hour": 00,
                "minute": 50,
                "second": 00,
            },
        })

        db.drop_table("todos")
        ret = db.table("todos")
        ret.insert({
            "job": {
                "name": "sample todo"
            },
            "once": {
                "year": 00,
                "month": 00,
                "day": 00,
                "hour": 00,
                "minute": 00,
                "second": 00,
            },
        })

        db.drop_table("commands")
        ct = db.table("commands")
        ct.insert({
            "command": "start",
            "text": "this is a start message!",
        })


def main():
    search_user(DB)
    print("OK")


if __name__ == "__main__":
    main()
