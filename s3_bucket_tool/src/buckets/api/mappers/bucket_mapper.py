from s3_bucket_tool.src.buckets.domain.bucket import Bucket
from s3_bucket_tool.src.buckets.domain.format import SizeFormat


def map_to_displayable(bucket: Bucket, size_format: SizeFormat) -> dict:
    return {
        "name": bucket.name,
        "creation_date": bucket.creation_date.strftime("%c"),
        "nb_files": bucket.nb_files,
        f"total_size ({size_format})": bucket.convert_unit(size_format),
        "last_modified": bucket.last_modified.strftime("%c") if bucket.last_modified else "Never",
        "cost": bucket.calculate_cost(),
    }
