from src.routes import search_object
from collections import namedtuple
from datetime import datetime

class mock_s3_client:
    def __init__(self, *args, **kwargs) -> None:
        ...

    def list_objects_v2(self, *args, **kwargs):
        return {
            'Contents': [
                {
                    'Key': 'abc/abc.txt',
                    'LastModified': datetime.strptime('2022-05-04', '%Y-%m-%d'),
                    'Size': 44,
                }
            ]
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


def test_if_test_filters_the_abc_file(monkeypatch):
    monkeypatch.setattr(search_object, 'get_constants', mock_get_constants)
    monkeypatch.setattr(search_object.boto3, 'client', mock_s3_client)

    bucket = 'abc'
    prefix = 'abc'
    search_term = 'abc'
    next_continuation_token = False

    res = search_object.search_object(bucket, prefix, search_term, next_continuation_token)
    
    assert res == {'next_continuation_token': False, 'objects': [{'name': 'abc.txt', 'last_modified': '2022-05-04', 'size': 44, 'key': 'abc/abc.txt'}]}
