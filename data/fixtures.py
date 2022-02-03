from tinydb import TinyDB, Query
import pathlib

FILE = pathlib.Path(__file__)
DIR = FILE.parent
DB = DIR / "db.json"



SAMPLE_DATA = [
    ()
]


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
    create_tinydb(DB)
    print("OK")


if __name__ == "__main__":
    main()
