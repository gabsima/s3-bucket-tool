from typing import AsyncGenerator
from s3_bucket_tool.src.buckets.domain.bucket_repository import BucketRepository
from s3_bucket_tool.src.buckets.domain.bucket import Bucket
from s3_bucket_tool.src.buckets.domain.enums import SupportedGrouping


class BucketGetter:
    def __init__(self, repo: BucketRepository):
        self.repo = repo

    async def get(self, name: str):
        print(f"Getting bucket with name {name}")
        return await self.repo.get_bucket(name)

    def stream(self) -> AsyncGenerator[Bucket, None]:
        print(f"Getting all buckets")
        return self.repo.list_buckets()

    async def filter_by_name(self, name: str) -> AsyncGenerator[Bucket, None]:
        print(f"Find buckets named {name}")
        async for bucket in self.repo.list_buckets():
            if name in bucket.name:
                yield bucket

    async def filter_by_storage_class(
        self, storage_class: str
    ) -> AsyncGenerator[Bucket, None]:
        print(f"Find buckets containg storage {storage_class}")
        async for bucket in self.repo.list_buckets():
            if storage_class in bucket.storage_classes:
                yield bucket

    async def group(self, group_by: SupportedGrouping):
        print(f"Getting all buckets groups by {group_by}")
        groups = {}
        async for bucket in self.repo.list_buckets():
            if bucket.location in groups:
                groups[bucket.location] = groups[bucket.location] + [bucket]
            else:
                groups[bucket.location] = [bucket]
        return groups
