import threading
from collections.abc import Callable


class ScanScheduler:
    def __init__(self) -> None:
        self._timers: list[threading.Timer] = []

    def schedule(self, interval_seconds: int, func: Callable[[], None]) -> None:
        timer = threading.Timer(interval_seconds, func)
        timer.daemon = True
        timer.start()
        self._timers.append(timer)

    def shutdown(self) -> None:
        for timer in self._timers:
            timer.cancel()
