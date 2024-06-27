from datetime import datetime
import pytest
from unittest.mock import patch
from s3_bucket_tool.src.buckets.domain.bucket import Bucket
from s3_bucket_tool.src.buckets.domain.enums import SizeFormat
from s3_bucket_tool.src.buckets.domain.unit_converter import (
    convert_units_from_bytes,
)

SIZE = 258


def test_bucket__when_convert_units_to_bytes__should_return_bucket_size():
    bucket = given_a_bucket_with_size(SIZE)

    assert bucket.convert_unit(SizeFormat.BYTES) == bucket.total_size_bytes


@pytest.mark.parametrize(
    "unit",
    [
        (SizeFormat.KILOBYTES),
        (SizeFormat.MEGABYTES),
        (SizeFormat.GIGABYTES),
        (SizeFormat.TERABYTES),
    ],
)
def test_bucket__when_convert_units_to_other_than_bytes__should_use_unit_converter(
    unit: SizeFormat,
):
    with patch.object(convert_units_from_bytes, "__call__"):
        bucket = given_a_bucket_with_size(SIZE)
        assert bucket.convert_unit(unit) != bucket.total_size_bytes


def test_bucket__calculate_cost():
    value_big_enough_to_cost = 123456789123
    bucket = given_a_bucket_with_size(value_big_enough_to_cost)
    expected_cost = 2.64
    assert bucket.calculate_cost() == expected_cost


def given_a_bucket_with_size(size: int):
    return Bucket("name", datetime.now(), 0, size, None, "us-east-1", set())
