import sys
from typing import Any, TextIO

from measuring.entities import Measurement
from measuring.enums import TimeUnit


def set_measurement_kind(measurement: Measurement, **_kw: Any) -> dict:
    if measurement.region:
        kind = "Region"
    elif measurement.function:
        kind = (
            "Function"
            if not measurement.function.is_coroutine
            else "Coroutine"
        )
    else:
        kind = "Unknown callable"

    return {"kind": kind}


def set_measurement_name(measurement: Measurement, **_kw: Any) -> dict:
    if measurement.region:
        name = measurement.region.name or "N/A"
    elif measurement.function:
        name = measurement.function.name
    else:
        name = "N/A"

    return {"name": name}


class ConsolePrinter:
    def __init__(
        self,
        stream: TextIO = sys.stdout,
        round_time_at: int = 3,
    ) -> None:
        self.stream = stream
        self.round_time_at = round_time_at

    def format_time(self, time: float) -> str:
        r = self.round_time_at
        return f"{time:.{r}f}"

    def __call__(
        self,
        measurement: Measurement,
        kind: str,
        name: str,
        **_kw: Any,
    ) -> dict:
        if measurement.time_unit is TimeUnit.NANOSECONDS:
            elapsed = int(measurement.elapsed)
        else:
            elapsed = self.format_time(measurement.elapsed)
        self.stream.write(
            f"{kind} {name!r} took {elapsed} {measurement.time_unit}.\n"
        )
        return {}
