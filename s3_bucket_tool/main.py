import typer
from s3_bucket_tool.src.buckets.domain.format import SizeFormat
from s3_bucket_tool.src.buckets.api.bucket_api import bucket_api

app = typer.Typer()


@app.command()
def get(
    bucket: str,
    size_format: SizeFormat = typer.Option(SizeFormat.BYTES, case_sensitive=False),
):
    bucket_api.get_bucket(bucket, size_format=size_format)


@app.command()
def list(
    size_format: SizeFormat = typer.Option(SizeFormat.BYTES, case_sensitive=False)
):
    bucket_api.list_buckets(size_format=size_format)


if __name__ == "__main__":
    app()
