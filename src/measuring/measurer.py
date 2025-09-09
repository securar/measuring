from collections.abc import Awaitable, Callable, Coroutine, Generator
from contextlib import contextmanager
from typing import Any, Final, ParamSpec, TypeVar

from measuring.api.protocols import Counter
from measuring.entities import (
    DefaultCounter,
    EventObserver,
    Measurement,
)
from measuring.enums import TimeUnit
from measuring.models import Function, Region
from measuring.processors import (
    ConsolePrinter,
    set_measurement_kind,
    set_measurement_name,
)
from measuring.utils import ProcessorType, dump_event_data, ensure_processors

P = ParamSpec("P")
T = TypeVar("T")

type Coro[**P, T] = Callable[P, Coroutine[Any, Any, T]]

DEFAULT_PROCESSORS: Final[list[ProcessorType]] = [
    set_measurement_kind,
    set_measurement_name,
    ConsolePrinter(),
]


class Measurer:
    def __init__(
        self,
        name: str | None = None,
        processors: list[ProcessorType] = DEFAULT_PROCESSORS,
        counter: Counter | None = None,
        time_unit: TimeUnit = TimeUnit.MILLISECONDS,
    ) -> None:
        if not name:
            name = hex(id(self))
        self.name = name
        self.processors = ensure_processors(processors)
        self.counter = counter or DefaultCounter(time_unit=time_unit)
        self.event_observer = EventObserver(self.processors)
        self.event_data = {}

    def update(self, **event_data: Any) -> None:
        event_data = self.event_observer.observe(**event_data)
        self.event_data.update(event_data)

    @contextmanager
    def region(self, name: str | None = None) -> Generator:
        """Measure region execution time.

        :param name: Region name

        Example:
        ```python
        measurer = Measurer()

        with measurer.region("loop"):
            for i in range(20_000_000):
                continue
        ```
        """
        self.counter.start()
        try:
            yield
        finally:
            self.counter.stop()
            measurement = Measurement(
                function=None,
                region=Region(name=name),
                elapsed=self.counter.elapsed,
                time_unit=self.counter.time_unit,
            )
            self.update(measurement=measurement)

    def func(self, func: Callable[P, T]) -> Callable[P, T]:
        """Measure function execution time.

        Example:
        ```python
        measurer = Measurer()

        @measurer.function
        def loop():
            for i in range(20_000_000):
                continue

        loop()
        ```
        """

        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            self.counter.start()
            result = func(*args, **kwargs)
            self.counter.stop()
            function = Function(
                name=func.__qualname__,
                func=func,
                args=args,
                kwargs=kwargs,
                is_coroutine=False,
            )
            measurement = Measurement(
                function=function,
                region=None,
                elapsed=self.counter.elapsed,
                time_unit=self.counter.time_unit,
            )
            self.update(measurement=measurement)
            return result

        return wrapper

    def coro(self, coro: Callable[P, Awaitable[T]]) -> Coro[P, T]:
        """Measure coroutine execution time.

        Example:
        ```python
        measurer = Measurer()

        @measurer.coroutine
        async def loop():
            for i in range(20_000_000):
                continue

        asyncio.run(loop())
        ```
        """

        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            self.counter.start()
            result = await coro(*args, **kwargs)
            self.counter.stop()
            function = Function(
                name=coro.__qualname__,
                func=coro,
                args=args,
                kwargs=kwargs,
                is_coroutine=True,
            )
            measurement = Measurement(
                function=function,
                region=None,
                elapsed=self.counter.elapsed,
                time_unit=self.counter.time_unit,
            )
            self.update(measurement=measurement)
            return result

        return wrapper
