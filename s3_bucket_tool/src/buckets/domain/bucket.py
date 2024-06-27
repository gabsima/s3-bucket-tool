from datetime import datetime
from typing import Optional, Set
from .enums import SizeFormat
from .unit_converter import convert_units_from_bytes


class Bucket:
    def __init__(
        self,
        name: str,
        creation_date: datetime,
        files_count: int,
        bucket_size: int,
        last_modified: Optional[datetime],
        location: str,
        bucket_storage_classes: Set[str],
    ):
        self.name = name
        self.creation_date = creation_date
        self.nb_files = files_count
        self.total_size_bytes = bucket_size
        self.last_modified = last_modified
        self.location = location
        self.storage_classes = bucket_storage_classes

    def calculate_cost(self):
        return round(0.023 * self.total_size_bytes / 1024 / 1024 / 1024, 2)

    def convert_unit(self, format: SizeFormat):
        if format == SizeFormat.BYTES:
            return self.total_size_bytes

        return convert_units_from_bytes(self.total_size_bytes, format)
