from time import perf_counter_ns as _default_counter

from measuring.api.protocols import Counter
from measuring.enums import TimeUnit


class DefaultCounter(Counter):
    def __init__(self, time_unit: TimeUnit) -> None:
        self._start_time: float
        self._elapsed: float
        
        self.counter = _default_counter
        self._time_unit = time_unit

    def convert_ns(self, ns: float) -> float:
        match self.time_unit:
            case TimeUnit.NANOSECONDS:
                return ns
            case TimeUnit.MILLISECONDS:
                return ns / 1_000_000
            case TimeUnit.SECONDS:
                return ns / 1_000_000_000
            case TimeUnit.MINUTES:
                return ns / 60_000_000_000
    
    def get_time(self) -> float:
        return self.convert_ns(self.counter())
    
    def start(self) -> None:
        self._start_time = self.get_time()

    def stop(self) -> None:
        self._elapsed = self.get_time() - self._start_time

    @property
    def elapsed(self) -> float:
        return self._elapsed

    @property
    def time_unit(self) -> TimeUnit:
        return self._time_unit
