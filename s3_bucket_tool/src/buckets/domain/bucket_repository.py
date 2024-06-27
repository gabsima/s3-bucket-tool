from abc import ABC, abstractmethod
from s3_bucket_tool.src.buckets.domain.bucket import Bucket
from typing import AsyncGenerator


class BucketRepository(ABC):
    @abstractmethod
    async def list_buckets(self) -> AsyncGenerator[Bucket, None]:
        pass

    @abstractmethod
    async def get_bucket(self, bucket: str) -> Bucket:
        pass
