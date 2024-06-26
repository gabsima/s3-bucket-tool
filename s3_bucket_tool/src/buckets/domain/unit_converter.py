from .format import SizeFormat
from decimal import Decimal


def bytes_to_kilobytes(bytes):
    return round(Decimal(bytes) / Decimal(1024))


def bytes_to_megabytes(bytes):
    return round(Decimal(bytes) / Decimal(1024**2))


def bytes_to_gigabytes(bytes):
    return round(Decimal(bytes) / Decimal(1024**3))


def bytes_to_terabytes(bytes):
    return round(Decimal(bytes) / Decimal(1024**4))


def convert_units_from_bytes(value, to_unit: SizeFormat):
    conversion_table = {
        SizeFormat.KILOBYTES: bytes_to_kilobytes,
        SizeFormat.MEGABYTES: bytes_to_megabytes,
        SizeFormat.GIGABYTES: bytes_to_gigabytes,
        SizeFormat.TERABYTES: bytes_to_terabytes,
    }

    if to_unit in conversion_table:
        return int(conversion_table[to_unit](value))
    else:
        raise ValueError(f"Conversion from bytes to {to_unit} not supported.")
