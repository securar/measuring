from collections.abc import Callable
from typing import Any

from measuring.api.protocols import Processor


class ProcessorImpl(Processor):
    def __init__(
        self,
        name: str,
        callable_obj: Callable[..., dict],
    ) -> None:
        self.name = name
        self.callable_obj = callable_obj

    def call(self, **event_data: Any) -> dict:
        return self.callable_obj(**event_data)
