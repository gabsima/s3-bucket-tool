import asyncio

import aioboto3
from typing import AsyncGenerator, Generator, List

import aioboto3.session
from s3_bucket_tool.src.buckets.domain.bucket_repository import BucketRepository
from s3_bucket_tool.src.buckets.domain.bucket import Bucket


def chunk_list(lst: List, chunk_size: int) -> Generator[List, None, None]:
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]


class S3BucketRepository(BucketRepository):
    CHUNK_SIZE = 30

    async def __get_bucket(self, client, resource, name: str) -> Bucket:
        paginator = client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=name)

        last_modified = None
        file_count = 0
        bucket_size = 0
        bucket_storage_classes = set()

        async for page in page_iterator:
            if "Contents" in page:
                for bucket_object in page["Contents"]:
                    last_modified = bucket_object["LastModified"]
                    file_count += 1
                    bucket_size += bucket_object["Size"]
                    bucket_storage_classes.add(bucket_object["StorageClass"])

        bucket = await resource.Bucket(name)
        creation_date = await bucket.creation_date
        location = await client.get_bucket_location(Bucket=name)

        return Bucket(
            name,
            creation_date,
            file_count,
            bucket_size,
            last_modified,
            location["LocationConstraint"],
            bucket_storage_classes,
        )

    async def get_bucket(self, name: str) -> Bucket:
        session = aioboto3.Session()
        async with session.resource("s3") as resource, session.client("s3") as client:
            return await self.__get_bucket(client, resource, name)

    async def list_buckets(self) -> AsyncGenerator[Bucket, None]:
        session = aioboto3.Session()
        async with session.resource("s3") as resource, session.client("s3") as client:
            response = await client.list_buckets()
            buckets = response.get("Buckets", [])

            for chunk in chunk_list(buckets, self.CHUNK_SIZE):
                tasks = [
                    asyncio.create_task(
                        self.__get_bucket(client, resource, bucket["Name"])
                    )
                    for bucket in chunk
                ]

                for task in asyncio.as_completed(tasks):
                    yield await task
