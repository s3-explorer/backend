import test.search_object as test_init

from src.routes import search_object


def convert_dict(objects):
    return [
        {
            'key': obj['Key'],
            'last_modified': obj['LastModified'].strftime('%Y-%m-%d'),
            'name': obj['Key'].split('/')[-1],
            'size': obj['Size'],
        }
        for obj in objects
    ]


def test_if_filters_the_abc_abc_x_files(pre_test):
    res = search_object.search_object(
        bucket='xpto',
        prefix='abc',
        search_term='abc',
        next_continuation_token=False,
    )

    assert res.get('objects') == convert_dict(test_init.object_with_abc_abc_x)


def test_if_filters_the_abc_xyz_x_files(pre_test):
    res = search_object.search_object(
        bucket='xpto',
        prefix='abc',
        search_term='xyz',
        next_continuation_token=False,
    )

    assert res.get('objects') == convert_dict(test_init.object_with_abc_xyz_x)


def test_if_filters_all_files_that_ends_with_txt(pre_test):
    res = search_object.search_object(
        bucket='abc',
        prefix='',
        search_term='.txt',
        next_continuation_token=False,
    )
    expected = (
        test_init.object_with_abc_abc_x
        + test_init.object_with_abc_xyz_x
        + test_init.object_with_xyz_abc_x
        + test_init.object_with_xyz_xyz_x
    )
    assert len(res.get('objects')) == len(expected)
