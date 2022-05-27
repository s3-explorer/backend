from src.routes import search_object
from collections import namedtuple
from datetime import datetime
from random import randint
from pytest import fixture


object_keys = [
    {
        'Key': f'abc/{f"abc_{i}" if i < 200 else f"xyz_{i}"}.txt',
        'LastModified': datetime.strptime(f'2022-{str(randint(1,12)).zfill(2)}-{str(randint(1,28)).zfill(2)}', '%Y-%m-%d'),
        'Size': randint(44,78924),
    } 
    for i in range(0,400)
]

class mock_s3_client:
    def __init__(self, *args, **kwargs) -> None:
        ...

    def list_objects_v2(self, *args, **kwargs):
        return {
            'Contents': object_keys
        }

def mock_get_constants():
    constants = namedtuple(
        'Constants', ['buckets_to_not_show', 'buckets_to_show', 'client_config']
    )
    buckets_to_not_show = 'xpto'
    buckets_to_show = 'xpto'
    client_config = {
        'service_name': 's3',
        'aws_access_key_id': '123456',
        'aws_secret_access_key': '123',
    }

    return constants(buckets_to_not_show, buckets_to_show, client_config)


@fixture
def pre_test(monkeypatch):
    monkeypatch.setattr(search_object, 'get_constants', mock_get_constants)
    monkeypatch.setattr(search_object.boto3, 'client', mock_s3_client)