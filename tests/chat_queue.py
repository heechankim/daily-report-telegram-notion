import logging
from queue import Queue
from threading import Thread

class ChatQueue:
    def __init__(
            self
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("ChatQueue init")
        self.MAXSIZE = 20
        self.me_reply = Queue(maxsize=self.MAXSIZE)
        self.bot_reply = Queue(maxsize=self.MAXSIZE)

    def bot_say(self, message: str):
        self.bot_reply.put_nowait(message)

    def me_say(self, message: str):
        self.me_reply.put_nowait(message)

    def bot_said(self):
        return self.bot_reply.get_nowait()

    def me_said(self):
        return self.me_reply.get_nowait()
