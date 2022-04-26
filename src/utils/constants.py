import os
from collections import namedtuple

Constants = namedtuple(
    'Constants', ['buckets_to_not_show', 'buckets_to_show', 'client_config']
)

buckets_to_not_show = os.getenv('BUCKETS_TO_NOT_SHOW', '')
buckets_to_show = os.getenv('BUCKETS_TO_SHOW', False)
endpoint_url = os.getenv('ENDPOINT_URL', False)
client_config = {
    'service_name': 's3',
    'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
}
if endpoint_url:
    client_config['endpoint_url'] = endpoint_url

constants = Constants(buckets_to_not_show, buckets_to_show, client_config)
