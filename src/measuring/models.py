from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from measuring.enums import TimeUnit


@dataclass
class Region:
    name: str | None


@dataclass
class Function:
    name: str
    func: Callable
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    is_coroutine: bool


@dataclass
class Measurement:
    function: Function | None
    region: Region | None

    elapsed: float
    time_unit: TimeUnit
