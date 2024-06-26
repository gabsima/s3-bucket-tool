import enum


class SizeFormat(str, enum.Enum):
    BYTES = "b"
    KILOBYTES = "kb"
    MEGABYTES = "mb"
    GIGABYTES = "gb"
    TERABYTES = "tb"
