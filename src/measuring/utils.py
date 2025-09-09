import json
from collections.abc import Callable
from dataclasses import asdict, is_dataclass
from json import JSONEncoder
from typing import Any

from measuring.api.protocols import Processor
from measuring.entities import ProcessorImpl

type ProcessorType = Callable[..., dict] | Processor


def is_dataclass_instance(obj: Any) -> bool:
    return is_dataclass(obj) and not isinstance(obj, type)


class EventDataEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if is_dataclass_instance(o):
            return asdict(o)

        if callable(o):
            return repr(o)

        return super().default(o)


def dump_event_data(event_data: dict, indent: int = 4) -> str:
    return json.dumps(
        event_data,
        indent=indent,
        ensure_ascii=False,
        cls=EventDataEncoder,
    )


def ensure_processors(processors: list[ProcessorType]) -> list[Processor]:
    ensured_processors = []

    for processor in processors:
        ensured = processor
        if callable(processor):
            ensured = ProcessorImpl(
                name=processor.__class__.__name__,
                callable_obj=processor,
            )
        ensured_processors.append(ensured)

    return ensured_processors
