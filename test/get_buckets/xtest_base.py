from os import environ
from src.utils.constants import constants


def test_if_constant_buckets_to_not_show_is_string():
    environ['BUCKETS_TO_NOT_SHOW'] = 'bucket-01'
    buckets_to_not_show = constants.buckets_to_not_show
    assert type(buckets_to_not_show) == str