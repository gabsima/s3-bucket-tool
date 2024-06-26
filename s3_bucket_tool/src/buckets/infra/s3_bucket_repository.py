from datetime import datetime

import boto3
from dateutil.tz import tzutc
from mypy_boto3_s3 import S3Client
from typing import Generator, List
from s3_bucket_tool.src.buckets.domain.bucket_repository import BucketRepository
from s3_bucket_tool.src.buckets.domain.bucket import Bucket


class S3BucketRepository(BucketRepository):
    def get_bucket(self, name: str) -> Bucket:
        client = boto3.client("s3")

        paginator = client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=name)

        last_modified = None
        file_count = 0
        bucket_size = 0

        for page in page_iterator:
            if "Contents" in page:
                for bucket_object in page["Contents"]:
                    last_modified = bucket_object["LastModified"]
                    file_count += 1
                    bucket_size += bucket_object["Size"]

        return Bucket(
            name,
            boto3.resource("s3").Bucket(name).creation_date,
            file_count,
            bucket_size,
            last_modified,
        )

    def list_buckets(self) -> Generator[Bucket, None, None]:
        client: S3Client = boto3.client("s3")

        for bucket in client.list_buckets()["Buckets"]:
            if bucket_info := self.get_bucket(bucket["Name"]):
                yield bucket_info
