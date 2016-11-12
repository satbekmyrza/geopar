from enum import Enum


class AngleState(Enum):
    KNOWN = 1
    UNKNOWN = -1


class EmptyException(Exception):
    pass
