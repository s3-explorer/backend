import boto3
from src.utils.constants import get_constants



def get_buckets():
    constants = get_constants()
    s3_client = boto3.client(**constants.client_config)
    response = s3_client.list_buckets()
    if constants.buckets_to_show:
        buckets = [
            bucket.get('Name')
            for bucket in response.get('Buckets', [])
            if bucket.get('Name') in constants.buckets_to_show.split(',')
        ]
    else:
        buckets = [
            bucket.get('Name')
            for bucket in response.get('Buckets', [])
            if bucket.get('Name')
            not in constants.buckets_to_not_show.split(',')
        ]
    del s3_client
    return buckets
