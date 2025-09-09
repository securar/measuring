from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


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
