from datetime import datetime
from s3_bucket_tool.src.buckets.domain.enums import SizeFormat
from s3_bucket_tool.src.buckets.domain.bucket import Bucket
from s3_bucket_tool.src.buckets.api.mappers.bucket_mapper import map_to_displayable


def test_bucket_mapper__given_no_last_modified_date__should_map_correctly():
    bucket = Bucket("name", datetime.now(), 26, 56, None, "us-east-1", set())

    value = map_to_displayable(bucket, SizeFormat.BYTES)

    assert value["last_modified"] == "Never"


def test_bucket_mapper__given_last_modified_date__should_map_correctly():
    date = "Tue Jun 25 20:09:10 2024"
    bucket = Bucket(
        "name",
        datetime.now(),
        26,
        56,
        datetime.strptime(date, "%c"),
        "us-east-1",
        set(),
    )

    value = map_to_displayable(bucket, SizeFormat.BYTES)

    assert value["last_modified"] == date


def test_bucket_mapper__should_map_correctly():
    date = "Tue Jun 25 20:09:10 2024"
    bucket = Bucket(
        "name", datetime.strptime(date, "%c"), 26, 56, None, "us-east-1", set()
    )

    value = map_to_displayable(bucket, SizeFormat.BYTES)

    assert value == {
        "name": "name",
        "creation_date": date,
        "nb_files": 26,
        f"total_size (b)": 56,
        "last_modified": "Never",
        "cost": 0,
    }
