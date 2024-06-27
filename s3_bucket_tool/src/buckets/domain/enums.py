import enum


class SizeFormat(str, enum.Enum):
    BYTES = "b"
    KILOBYTES = "kb"
    MEGABYTES = "mb"
    GIGABYTES = "gb"
    TERABYTES = "tb"


class SupportedGrouping(str, enum.Enum):
    REGION = "region"


class StorageClass(str, enum.Enum):
    STANDARD = ("standard",)
    INFREQUENT = ("ia",)
    RARE = "rr"
