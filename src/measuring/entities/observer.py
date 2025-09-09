from typing import Any

from measuring.api.protocols import Processor


class EventObserver:
    def __init__(self, processors: list[Processor]) -> None:
        self.processors = processors

    def observe(self, **event_data: Any) -> dict:
        new_data = event_data.copy()
        for processor in self.processors:
            data = processor.call(**new_data)
            new_data.update(data)
        return new_data
