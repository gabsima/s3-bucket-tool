from typing import Optional
import typer
from s3_bucket_tool.src.buckets.domain.enums import SizeFormat, SupportedGrouping
from s3_bucket_tool.src.buckets.api.bucket_api import bucket_api
from functools import wraps
from asyncio import get_event_loop
import typer

from functools import wraps


def async_command(app, *args, **kwargs):
    def decorator(async_func):

        @wraps(async_func)
        def sync_func(*_args, **_kwargs):
            return get_event_loop().run_until_complete(async_func(*_args, **_kwargs))

        app.command(*args, **kwargs)(sync_func)
        return async_func

    return decorator


typer.Typer.async_command = async_command

app = typer.Typer()


@app.async_command()
async def get(
    bucket: str,
    size_format: SizeFormat = typer.Option(SizeFormat.BYTES, case_sensitive=False),
):
    await bucket_api.get_bucket(bucket, size_format=size_format)


@app.async_command()
async def find(
    name: str = typer.Option(None),
    storage_class: str = typer.Option(None),
    size_format: SizeFormat = typer.Option(SizeFormat.BYTES),
):
    if (name is not None and storage_class is not None) or (
        name is None and storage_class is None
    ):
        print("Either one of name or storage class must be provided")
        return

    if name is not None:
        await bucket_api.filter_by_name(name, size_format)

    if storage_class is not None:
        await bucket_api.filter_by_storage_class(storage_class, size_format)


@app.async_command()
async def list(
    size_format: SizeFormat = typer.Option(SizeFormat.BYTES, case_sensitive=False),
    group_by: Optional[SupportedGrouping] = typer.Option(None),
):
    await bucket_api.list_buckets(size_format=size_format, group_by=group_by)


if __name__ == "__main__":
    app()
