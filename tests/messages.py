from threading import Thread, Lock
from queue import Queue

from typing import Callable


# q = Queue()
#
#
# def consumer():
#     print("Consumer Waiting")
#     work = q.get()
#     print("Consumer Working")
#
#     print(work)
#
#     print("Consumer done")
#     q.task_done()
#
#
# thread = Thread(target=consumer).start()
#
#
# """
# 이제 생산자는 조인으로 소비 스레드를 대기하거나 폴링하지 않아도 됨.
#
# 그냥 Queue 인스턴스의 join 을 호출해 q 가 완료하기를 기다리면됨.
#
# 심지어 큐가 비더라도 q 의 join 메서드는 이미 큐에 추가된 모든 아이템에 task_done 을 호출할 때까지 완료하지 않음
# """
#
# q.put("This is a Queue item")
# print("Producer waiting")
# q.join()
# print("Producer done")
def callee(msg):
    print("        this is callee")
    print("                " + msg)
    print("        callee done")


class Messages:
    def __init__(
            self
    ):
        self.bot = Queue(maxsize=10)
        self.me = Queue(maxsize=10)
        self.__thread = Thread(target=self.from_bot, args=(callee, ))
        self.__thread.start()

    def bot_said(self, msg: str):
        self.bot.put(msg)
        print("Producer waiting")
        print(self.bot.unfinished_tasks)
        self.bot.join()
        print("Producer done")

    def from_bot(self, callback: Callable[[str], None]):
        while True:
            print("    Consumer Waiting")
            msg = self.bot.get()
            print("    Consumer Working")
            if msg is None:
                break
            callback(msg)
            self.bot.task_done()
        print("    Consumer done")

    def stop(self):
        print(self.__thread.is_alive())
        self.__thread._tstate_lock.release()


if __name__ == "__main__":
    m = Messages()

    m.bot_said("This is a new messages")
    m.bot_said("This is a new messages1")
    m.bot_said("This is a new messages2")

    print("all done")
    m.stop()



