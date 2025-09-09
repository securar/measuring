from abc import abstractmethod
from typing import Any, Protocol

from measuring.enums import TimeUnit


class Processor(Protocol):
    @abstractmethod
    def call(self, **event_data: Any) -> dict:
        raise NotImplementedError


class Counter(Protocol):
    @abstractmethod
    def convert_ns(self, ns: float) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def get_time(self) -> float:
        raise NotImplementedError
    
    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def elapsed(self) -> float:
        raise NotImplementedError

    @property
    @abstractmethod
    def time_unit(self) -> TimeUnit:
        raise NotImplementedError
