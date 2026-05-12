import os
import time
import uuid
from functools import lru_cache
from typing import Any

import boto3
from botocore.client import BaseClient


def _client_kwargs() -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    region = os.getenv("AWS_REGION")
    if region:
        kwargs["region_name"] = region

    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    session_token = os.getenv("AWS_SESSION_TOKEN")

    if access_key and secret_key:
        kwargs["aws_access_key_id"] = access_key
        kwargs["aws_secret_access_key"] = secret_key
        if session_token:
            kwargs["aws_session_token"] = session_token

    return kwargs


@lru_cache(maxsize=1)
def get_s3_client() -> BaseClient:
    return boto3.client("s3", **_client_kwargs())


@lru_cache(maxsize=1)
def get_sns_client() -> BaseClient:
    return boto3.client("sns", **_client_kwargs())


@lru_cache(maxsize=1)
def get_dynamodb_client() -> BaseClient:
    return boto3.client("dynamodb", **_client_kwargs())


def upload_profile_picture(*, alumno_id: int, filename: str, content_type: str | None, fileobj: Any) -> str:
    bucket = os.getenv("S3_BUCKET_NAME")
    if not bucket:
        raise RuntimeError("S3 bucket is not configured")

    extension = os.path.splitext(filename or "")[1] or ".jpg"
    key = f"alumnos/{alumno_id}/profile-{uuid.uuid4().hex}{extension}"

    extra_args = {"ACL": "public-read", "ContentType": content_type or "application/octet-stream"}
    get_s3_client().upload_fileobj(fileobj, bucket, key, ExtraArgs=extra_args)

    return f"https://{bucket}.s3.amazonaws.com/{key}"


def publish_alumno_email(message: str) -> None:
    topic_arn = os.getenv("SNS_TOPIC_ARN")
    if not topic_arn:
        raise RuntimeError("SNS topic ARN is not configured")

    get_sns_client().publish(TopicArn=topic_arn, Message=message, Subject="Calificaciones alumno")


def create_session_item(*, alumno_id: int, session_string: str) -> None:
    table_name = os.getenv("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise RuntimeError("DynamoDB table name is not configured")

    item = {
        "id": {"S": str(uuid.uuid4())},
        "fecha": {"N": str(int(time.time()))},
        "alumnoId": {"N": str(alumno_id)},
        "active": {"BOOL": True},
        "sessionString": {"S": session_string},
    }

    get_dynamodb_client().put_item(TableName=table_name, Item=item)


def find_session_item(*, alumno_id: int, session_string: str) -> dict[str, Any] | None:
    table_name = os.getenv("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise RuntimeError("DynamoDB table name is not configured")

    response = get_dynamodb_client().scan(
        TableName=table_name,
        FilterExpression="alumnoId = :aid AND sessionString = :ss",
        ExpressionAttributeValues={
            ":aid": {"N": str(alumno_id)},
            ":ss": {"S": session_string},
        },
    )

    items = response.get("Items", [])
    if not items:
        return None

    return items[0]


def deactivate_session_item(item: dict[str, Any]) -> None:
    table_name = os.getenv("DYNAMODB_TABLE_NAME")
    if not table_name:
        raise RuntimeError("DynamoDB table name is not configured")

    session_id = item.get("id", {}).get("S")
    if not session_id:
        raise RuntimeError("Session item is missing id")

    get_dynamodb_client().update_item(
        TableName=table_name,
        Key={"id": {"S": session_id}},
        UpdateExpression="SET active = :false",
        ExpressionAttributeValues={":false": {"BOOL": False}},
    )
