"""User Entities"""


class User:
    def __init__(
            self,
            chat_id: int,
            pages: dict = dict(root="", daily=""),
            integration: str = "",
    ):

        self.chat_id = chat_id
        self.pages = pages
        self.integration = integration
