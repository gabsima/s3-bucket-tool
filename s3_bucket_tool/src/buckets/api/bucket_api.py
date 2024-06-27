from typing import AsyncGenerator, Optional
from s3_bucket_tool.src.buckets.domain.bucket import Bucket
from s3_bucket_tool.src.buckets.services.bucket_getter import BucketGetter
from s3_bucket_tool.src.buckets.infra.s3_bucket_repository import (
    S3BucketRepository,
)
from s3_bucket_tool.src.buckets.domain.enums import SizeFormat, SupportedGrouping
from .mappers.bucket_mapper import map_to_displayable
import lazy_table as lt
from tabulate import tabulate


class BucketApi:
    def __init__(self, bucket_getter: BucketGetter):
        self.bucket_getter = bucket_getter

    async def get_bucket(self, name: str, size_format: Optional[SizeFormat]):
        bucket = await self.bucket_getter.get(name)
        if bucket:
            print(tabulate([map_to_displayable(bucket, size_format)], headers="keys"))

    async def filter_by_name(
        self, name: str, size_format: Optional[SizeFormat]
    ) -> AsyncGenerator[Bucket, None]:
        async for bucket in self.bucket_getter.filter_by_name(name):
            print(
                tabulate(
                    [map_to_displayable(bucket, size_format)],
                    headers="keys",
                    tablefmt="pretty",
                )
            )

    async def filter_by_storage_class(
        self, storage_class: str, size_format: Optional[SizeFormat]
    ) -> AsyncGenerator[Bucket, None]:
        async for bucket in self.bucket_getter.filter_by_storage_class(storage_class):
            print(
                tabulate(
                    [map_to_displayable(bucket, size_format)],
                    headers="keys",
                    tablefmt="pretty",
                )
            )

    async def list_buckets(
        self, size_format: Optional[SizeFormat], group_by: Optional[SupportedGrouping]
    ):
        if group_by:
            groups = await self.bucket_getter.group(group_by)
            for region, buckets in groups.items():
                print(region)
                print(
                    tabulate(
                        [map_to_displayable(bucket, size_format) for bucket in buckets],
                        headers="keys",
                        tablefmt="pretty",
                    )
                )
        else:
            async for bucket in self.bucket_getter.stream():
                print(
                    tabulate(
                        [map_to_displayable(bucket, size_format)],
                        headers="keys",
                        tablefmt="pretty",
                    )
                )


bucket_repo = S3BucketRepository()
bucket_getter = BucketGetter(bucket_repo)
bucket_api = BucketApi(bucket_getter)
