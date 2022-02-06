from DailyReport.databases.database import Database


class NotionDatabase:
    def __init__(self, db: Database):
        self.db = db

    def new_user(self, telegram_id: int, root_page_id: str):
        self.db.init_user(telegram_id, root_page_id)
        return self.db.is_user(telegram_id)

    def report(self, telegram_id: int):
        return self.db.is_user(telegram_id)
