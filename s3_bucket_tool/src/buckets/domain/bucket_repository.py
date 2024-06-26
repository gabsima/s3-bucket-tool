from abc import ABC, abstractmethod
from s3_bucket_tool.src.buckets.domain.bucket import Bucket
from typing import Generator, List


class BucketRepository(ABC):
    @abstractmethod
    def list_buckets(self) -> Generator[Bucket, None, None]:
        pass

    @abstractmethod
    def get_bucket(self, bucket: str) -> Bucket:
        pass
