from typing import Any

from measuring import Measurer
from measuring.enums import TimeUnit
from measuring.processors import (
    ConsolePrinter,
    set_measurement_kind,
    set_measurement_name,
)
from measuring.utils import dump_event_data


def event_data_printer(**event_data: Any) -> dict:
    data = dump_event_data(event_data)
    print(f"Event data: {data}")
    return {}


def set_my_data(**_kw: Any) -> dict:
    return {"my_data": 42}


processors = [
    set_measurement_kind,
    set_measurement_name,
    set_my_data,
    event_data_printer,
    ConsolePrinter(),
]

measurer = Measurer(processors=processors, time_unit=TimeUnit.MILLISECONDS)


@measurer.func
def loop(*_args: Any, **_kwargs: Any) -> None:
    for _ in range(20_000_00):
        continue


loop(42, foo="bar")
