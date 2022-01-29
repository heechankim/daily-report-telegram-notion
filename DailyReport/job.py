

class DailyJob:
    def __init__(
            self,
            callback: callable,
    ):
        self._callback = callback

    def __call__(self):
        self._callback()
