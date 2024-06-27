import pytest
from s3_bucket_tool.src.buckets.domain.enums import SizeFormat
from s3_bucket_tool.src.buckets.domain.unit_converter import (
    convert_units_from_bytes,
)

SIZE_VALUE_IN_BYTES = 1099511627776

testdata = [
    (SizeFormat.KILOBYTES, 1073741824),
    (SizeFormat.MEGABYTES, 1048576),
    (SizeFormat.GIGABYTES, 1024),
    (SizeFormat.TERABYTES, 1),
]


@pytest.mark.parametrize("unit,expected", testdata)
def test_unit_conversion(unit: SizeFormat, expected: float):
    assert convert_units_from_bytes(SIZE_VALUE_IN_BYTES, unit) == expected
