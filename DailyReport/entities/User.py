"""User Entities"""

from tinydb import TinyDB, where


class User:
    def __init__(
            self,
            chat_id: int,
            pages: dict,
            integration: str,
    ):

        self.chat_id = chat_id
        self.root = pages['root']
        self.daily = pages['daily']
        self.integration = integration
