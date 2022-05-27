from collections import namedtuple
from src.routes import get_buckets
from test.get_buckets import mock_s3_client

constants = namedtuple(
    'Constants', ['buckets_to_not_show', 'buckets_to_show', 'client_config']
)

client_config = {
    'service_name': 's3',
    'aws_access_key_id': '123456',
    'aws_secret_access_key': '123',
}

def test_if_return_all_buckets_when(monkeypatch):
    """Vou passar buckets_to_show e buckets_to_not_show vazios, assim não terá restrição
        do que retornar, logo deve retornar todos os buckets
    """

    def mock_get_constants():
        buckets_to_not_show = ''
        buckets_to_show = False
        return constants(buckets_to_not_show, buckets_to_show, client_config)

    monkeypatch.setattr(get_buckets, 'get_constants', mock_get_constants)
    monkeypatch.setattr(get_buckets.boto3, 'client', mock_s3_client)

    res = get_buckets.get_buckets()
    assert res == ['my-bkt-01', 'my-bkt-02', 'my-bkt-03', 'my-bkt-04']

def test_if_will_cut_the_buckets_in_buckets_to_not_show(monkeypatch):
    """Testar se irá cortar os buckets indicados em buckets_to_not_show"""
    def mock_get_constants():
        buckets_to_not_show = 'my-bkt-01,my-bkt-03'
        buckets_to_show = False
        return constants(buckets_to_not_show, buckets_to_show, client_config)

    monkeypatch.setattr(get_buckets, 'get_constants', mock_get_constants)
    monkeypatch.setattr(get_buckets.boto3, 'client', mock_s3_client)

    res = get_buckets.get_buckets()
    assert res == ['my-bkt-02', 'my-bkt-04']

def test_if_will_return_only_the_buckets_that_are_in_the_buckets_to_show(monkeypatch):
    "testar se irá retornar apenas o que está indicado em buckets_to_show"
    
    def mock_get_constants():
        buckets_to_not_show = ''
        buckets_to_show = 'my-bkt-01,my-bkt-02'
        return constants(buckets_to_not_show, buckets_to_show, client_config)

    monkeypatch.setattr(get_buckets, 'get_constants', mock_get_constants)
    monkeypatch.setattr(get_buckets.boto3, 'client', mock_s3_client)

    res = get_buckets.get_buckets()
    assert res == ['my-bkt-01', 'my-bkt-02']

def test_if_will_respect_the_buckets_to_show_instead_of_buckets_to_not_show(monkeypatch):
    """testar se irá respeitar o buckets_to_show no lugar do buckets_to_not_show"""
    def mock_get_constants():
        buckets_to_not_show = 'my-bkt-01,my-bkt-02'
        buckets_to_show = 'my-bkt-01,my-bkt-02'
        return constants(buckets_to_not_show, buckets_to_show, client_config)

    monkeypatch.setattr(get_buckets, 'get_constants', mock_get_constants)
    monkeypatch.setattr(get_buckets.boto3, 'client', mock_s3_client)

    res = get_buckets.get_buckets()
    assert res == ['my-bkt-01', 'my-bkt-02']
