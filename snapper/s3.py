import io
import logging
import os
from pathlib import Path

import aiobotocore
import boto3
from botocore.exceptions import ClientError


class S3:
    _instance = None

    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_bucket_name):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_bucket_name = aws_bucket_name

        try:
            self.sync_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                                            aws_secret_access_key=aws_secret_access_key)
            S3._instance = self
        except ClientError as e:
            logging.error(e.response['Error']['Message'])

    @staticmethod
    def get_instance():
        if not S3._instance:
            logging.error("S3 is not initialized")
        return S3._instance

    def upload_dir(self, source_dir, dest_dir):
        if self is None:
            logging.error("Storage is not initialized")
            return

        try:
            for root, dirs, files in os.walk(source_dir):
                for filename in files:
                    local_path = Path(root) / filename
                    relative_path = local_path.relative_to(source_dir)
                    s3_path = Path(dest_dir) / relative_path

                    with open(local_path, 'rb') as file_to_upload:
                        self.sync_client.put_object(Bucket=self.aws_bucket_name, Key=str(s3_path),
                                                    Body=file_to_upload.read())
        except ClientError as e:
            logging.error(e.response['Error']['Message'])

    def get_async_client(self):
        try:
            session = aiobotocore.get_session()
            return session.create_client('s3', aws_access_key_id=self.aws_access_key_id,
                                         aws_secret_access_key=self.aws_secret_access_key)
        except ClientError as e:
            logging.error(e.response['Error']['Message'])

    async def list_objects(self, async_client, prefix):
        try:
            response = await async_client.list_objects(Bucket=self.aws_bucket_name, Prefix=prefix)

            if 'Contents' not in response:
                return []
            else:
                return [object['Key'] for object in response['Contents']]
        except ClientError as e:
            logging.error(e.response['Error']['Message'])
            return []

    async def download_object(self, async_client, object, filename):
        try:
            response = await async_client.get_object(Bucket=self.aws_bucket_name, Key=object)
            async with response['Body'] as stream:
                with io.FileIO(filename, 'w') as file:
                    file.write(await stream.read())
        except ClientError as e:
            logging.error(e.response['Error']['Message'])
