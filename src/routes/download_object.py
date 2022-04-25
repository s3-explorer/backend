import boto3
from botocore.client import Config
from flask import request

from src.utils.constants import constants


def download_object():
    bucket = request.headers.get('x-bucket', False)
    key_name = request.headers.get('x-key-name', '')

    if not key_name:
        return 'Caminho do arquivo inválido', 400
    if not bucket:
        return 'Bucket inválido', 400

    try:
        s3_client = boto3.client(**constants.client_config)
        response = s3_client.get_bucket_location(Bucket=bucket)
        location = response.get('LocationConstraint')
        del s3_client
    except Exception as e:
        print(e)
        return 'Esse bucket não existe', 400

    s3_client = boto3.client(
        **constants.client_config,
        config=Config(signature_version='s3v4', region_name=location)
    )
    url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': key_name,
            'ResponseContentType': 'application/octet-stream',
        },
        ExpiresIn=2,
        HttpMethod='GET',
    )
    del s3_client
    return url
