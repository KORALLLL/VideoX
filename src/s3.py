import logging

import boto3
import botocore
import botocore.exceptions

from src.config import cfg


class S3:
    def __init__(self):
        self.session = boto3.session.Session(
            aws_access_key_id=cfg.s3.aws_access_key,
            aws_secret_access_key=cfg.s3.aws_secret_access_key,
            region_name=cfg.s3.aws_region,
        )
        self.s3client = self.session.client(
            service_name="s3",
            endpoint_url=cfg.s3.aws_host,
        )
        self.create_bucket(cfg.s3.aws_bucket)

    def has_file(self, fileid: str):
        try:
            self.s3client.head_object(Bucket=cfg.s3.aws_bucket, Key=fileid)
            return True
        except botocore.exceptions.ClientError:
            return False

    def upload_file(self, file, fileid: str):
        self.s3client.upload_fileobj(file, cfg.s3.aws_bucket, fileid)

    def download_file(self, file, fileid: str):
        try:
            self.s3client.head_object(Bucket=cfg.s3.aws_bucket, Key=fileid)
            self.s3client.download_fileobj(cfg.s3.aws_bucket, fileid, file)
            file.seek(0)
        except botocore.exceptions.ClientError:
            raise FileNotFoundError("File not found")

    def delete_file(self, fileid: str):
        self.s3client.delete_object(Bucket=cfg.s3.aws_bucket, Key=fileid)

    def create_bucket(self, name):
        try:
            try:
                self.s3client.head_bucket(Bucket=name)
                return
            except botocore.exceptions.ClientError:
                pass
            self.s3client.create_bucket(Bucket=name)
        except botocore.exceptions.ClientError as e:
            raise e
        except Exception as ex:
            logging.info(ex)

    def generate_link(self, bucket, key):
        return self.s3client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=3600,
        )


s3 = S3()
