import logging
from queue import Queue


class ChatQueue:
    def __init__(
            self
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("ChatQueue init")
        self.MAXSIZE = 20
        self.me = Queue(maxsize=self.MAXSIZE)
        self.bot = Queue(maxsize=self.MAXSIZE)
