from typing import Generator
from s3_bucket_tool.src.buckets.domain.bucket_repository import BucketRepository
from s3_bucket_tool.src.buckets.domain.bucket import Bucket

class BucketGetter:
    def __init__(self, repo: BucketRepository):
        self.repo = repo
    
    def get(self, name: str):
        print(f"Getting bucket with name {name}")
        return self.repo.get_bucket(name)
    
    def list(self) -> Generator[Bucket, None, None]:
        print(f"Getting all buckets")
        return self.repo.list_buckets()