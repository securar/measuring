from abc import abstractmethod
from collections.abc import Callable, Generator
from contextlib import contextmanager
from dataclasses import dataclass
from time import perf_counter
from typing import Any, Protocol, runtime_checkable

EventData = dict[str, Any]


@dataclass
class RegionMeasurement:
    name: str | None
    elapsed: float


@runtime_checkable
class Processor(Protocol):
    @abstractmethod
    def call(self, **event_data: Any) -> EventData:
        raise NotImplementedError
ProcessorType = Processor | Callable[..., EventData]

class FuncProcessor(Processor):
    def __init__(self, processor: Callable[..., EventData]) -> None:
        self.processor = processor

    def call(self, **event_data: Any) -> EventData:
        return self.processor(**event_data)


def ensure_processors(
    processors: list[],
) -> list[Processor]:
    ensured_processors = []

    for processor in processors:
        ensured = processor
        if callable(processor):
            ensured = FuncProcessor(processor)
        ensured_processors.append(ensured)

    return ensured_processors


class Counter(Protocol):
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


class DefaultCounter(Counter):
    def __init__(self) -> None:
        super().__init__()
        self.start_time: float
        self._elapsed: float

    def start(self) -> None:
        self.start_time = perf_counter()

    def stop(self) -> None:
        end_time = perf_counter()
        self._elapsed = end_time - self.start_time

    @property
    def elapsed(self) -> float:
        return self._elapsed


class EventObserver:
    def __init__(self, processors: list[Processor]) -> None:
        self.processors = processors

    def observe(self, **event_data: Any) -> None:
        for processor in self.processors:
            processor.call(**event_data)


class Measurer:
    def __init__(
        self,
        processors: list[Processor],
        counter: Counter | None = None,
    ) -> None:
        self.processors = processors
        self.counter = counter or DefaultCounter()
        self.event_observer = EventObserver(processors)
        self.event_data = {}

    @contextmanager
    def region(self, name: str | None = None) -> Generator:
        self.counter.start()
        try:
            yield
        finally:
            self.counter.stop()
            measurement = RegionMeasurement(
                name=name,
                elapsed=self.counter.elapsed,
            )
            self.event_observer.observe(measurement=measurement)
