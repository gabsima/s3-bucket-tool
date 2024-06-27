from datetime import datetime
from typing import Set
from unittest.mock import Mock

import pytest
from s3_bucket_tool.src.buckets.domain.bucket import Bucket
from s3_bucket_tool.src.buckets.domain.enums import SupportedGrouping
from s3_bucket_tool.src.buckets.services.bucket_getter import BucketGetter


class AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration


@pytest.mark.asyncio
async def test_bucket_getter__when_groups_from_multiple_region__should_accumulate_correctly():
    repo = Mock()
    repo.list_buckets.return_value = AsyncIterator(
        [
            given_a_bucket(region="us-east-1"),
            given_a_bucket(region="us-east-2"),
            given_a_bucket(region="us-east-1"),
        ]
    )
    bucket_getter = BucketGetter(repo)

    res = await bucket_getter.group(SupportedGrouping.REGION)

    assert len(res["us-east-1"]) == 2
    assert len(res["us-east-2"]) == 1


@pytest.mark.asyncio
async def test_bucket_getter__when_find_by_name__should_gets_only_buckets_with_same_name():
    repo = Mock()
    repo.list_buckets.return_value = AsyncIterator(
        [
            given_a_bucket(name="nameA"),
            given_a_bucket(name="nameB"),
            given_a_bucket(name="totally-different"),
        ]
    )
    bucket_getter = BucketGetter(repo)

    res = []
    async for result in bucket_getter.filter_by_name("name"):
        res += [result]

    assert len(res) == 2
    assert len([b for b in res if b.name == "totaly-different"]) == 0


@pytest.mark.asyncio
async def test_bucket_getter__when_find_by_storage_class__should_gets_only_buckets_containing_said_class():
    repo = Mock()
    repo.list_buckets.return_value = AsyncIterator(
        [
            given_a_bucket(classes={"STANDARD", "RARE"}),
            given_a_bucket(classes={"STANDARD"}),
            given_a_bucket(classes={"INFREQUENT"}),
        ]
    )
    bucket_getter = BucketGetter(repo)

    res = []
    async for result in bucket_getter.filter_by_storage_class("STANDARD"):
        res += [result]

    assert len(res) == 2
    assert len([b for b in res if "INFREQUENT" in b.storage_classes]) == 0


def given_a_bucket(
    region: str = "us-east-1", name: str = "name", classes: Set[str] = set()
) -> Bucket:
    return Bucket(name, datetime.now(), 156, 123, None, region, classes)
