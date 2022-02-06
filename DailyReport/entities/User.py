"""User Entities"""

from tinydb import TinyDB, where


class User:
    def __init__(
            self,
            id: int,
            pages: dict,
            integration: str,
    ):

        self.id = int(id)
        self.root = pages['root']
        self.daily = pages['daily']
        self.integration = str(integration)
