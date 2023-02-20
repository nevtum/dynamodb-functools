from datetime import datetime, timedelta
from typing import Optional

import boto3


class DynamoDbBackend:
    def __init__(self, table_name):
        dynamodb = boto3.resource("dynamodb")
        self.table = dynamodb.Table(table_name)

    def get(self, hash_key: str) -> Optional[str]:
        response = self.table.get_item(
            Key={"{{cookiecutter.table.key_name}}": hash_key}
        )
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200
        item = response.get("Item")
        if not item:
            return
        return item["value"].value.decode("utf-8")

    def save(self, hashkey: str, value: str, ttl: timedelta):
        expiry_time = datetime.now() + ttl
        return self.table.put_item(
            Item={
                "{{cookiecutter.table.key_name}}": hashkey,
                "value": value,
                "{{cookiecutter.table.ttl_name}}": int(expiry_time.timestamp())
            }
        )
