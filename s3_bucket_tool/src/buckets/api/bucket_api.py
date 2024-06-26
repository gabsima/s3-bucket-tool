from typing import Optional
from s3_bucket_tool.src.buckets.services.bucket_getter import BucketGetter
from s3_bucket_tool.src.buckets.infra.s3_bucket_repository import (
    S3BucketRepository,
)
from s3_bucket_tool.src.buckets.domain.format import SizeFormat
from .mappers.bucket_mapper import map_to_displayable
import lazy_table as lt


class BucketApi:
    def __init__(self, bucket_getter: BucketGetter):
        self.bucket_getter = bucket_getter

    def get_bucket(self, name: str, size_format: Optional[SizeFormat]):
        if bucket := self.bucket_getter.get(name):
            lt.stream([map_to_displayable(bucket, size_format)], headers="keys")

    def list_buckets(self, size_format: Optional[SizeFormat]):
        buckets = self.bucket_getter.list()
        lt.stream((map_to_displayable(bucket, size_format) for bucket in buckets), headers="keys")
        

bucket_repo = S3BucketRepository()
bucket_getter = BucketGetter(bucket_repo)
bucket_api = BucketApi(bucket_getter)
