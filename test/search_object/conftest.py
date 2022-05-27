from collections import namedtuple
from test.search_object import mock_s3_client

from pytest import fixture

from src.routes import search_object


def mock_get_constants():
    constants = namedtuple(
        'Constants',
        ['buckets_to_not_show', 'buckets_to_show', 'client_config'],
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
