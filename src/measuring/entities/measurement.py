from dataclasses import dataclass

from measuring.enums import TimeUnit
from measuring.models import Function, Region


@dataclass
class Measurement:
    function: Function | None
    region: Region | None

    elapsed: float
    time_unit: TimeUnit
