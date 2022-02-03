import threading
from threading import Thread, Event
from queue import Queue

from typing import Callable


class Messages:
    def __init__(
            self,
            callback: Callable[[str], None],
    ):
        self.q = Queue()

        self.__th = Thread(target=self.consumer, args=(callback,))
        self.__th.start()

        self._stop = Event()

    def received(self, msg: str):
        self.q.put(msg)
        self.q.join()

    def consumer(self, callback: Callable[[str], None]):
        while True:
            msg = self.q.get()
            if msg is None:
                break
            callback(msg)
            self.q.task_done()

    def stop(self):
        self._stop.set()

    def stopped(self):
        print(self._stop.is_set())
        return self._stop.is_set()


# class Messages:
#     def __init__(
#             self,
#             bot_message_callback: Callable[[str], None],
#             my_message_callback: Callable[[str], None],
#     ):
#         self.bot = Queue(maxsize=10)
#         self.me = Queue(maxsize=10)
#
#         self.__bot_thread = Thread(target=self.from_bot, args=(bot_message_callback,))
#         self.__bot_thread.start()
#         self.__me_thread = Thread(target=self.from_me, args=(my_message_callback,))
#         self.__me_thread.start()
#
#         self._stop = threading.Event()
#
#
#     def bot_said(self, msg: str):
#         self.bot.put(msg)
#         self.bot.join()
#
#     def from_bot(self, callback: Callable[[str], None]):
#         while True:
#             msg = self.bot.get()
#             if self.stopped:
#                 break
#             callback(msg)
#             self.bot.task_done()
#
#     def me_said(self, msg: str):
#         self.me.put(msg)
#         self.me.join()
#
#     def from_me(self, callback: Callable[[str], None]):
#         while True:
#             msg = self.me.get()
#             if self.stopped:
#                 break
#             callback(msg)
#             self.me.task_done()
#
#     def stop(self):
#         self._stop.set()
#
#     def stopped(self):
#         print(self._stop.is_set())
#         return self._stop.is_set()


