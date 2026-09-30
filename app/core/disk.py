import re
import boto3
from botocore.client import Config

from app.core import log
from app.core.config import settings

s3 = boto3.client(
    "s3",
    endpoint_url=settings.AWS_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
    config=Config(
        signature_version="s3v4",
        s3={"addressing_style": "path"},
    ),
)

bucket_name = settings.AWS_BUCKET_NAME


def initialize_s3_bucket():
    try:
        s3.create_bucket(Bucket=bucket_name)
        log.info(f"Bucket {bucket_name} created.")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        log.warn(f"Bucket {bucket_name} already exists")


def s3_download(file_path: str, filename: str):
    return s3.download_file(bucket_name, file_path, filename)
