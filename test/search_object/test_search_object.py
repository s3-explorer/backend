from src.routes import search_object


def test_if_filters_the_200_abc_files(pre_test):
    res = search_object.search_object(
        bucket = 'abc',
        prefix = 'abc',
        search_term = 'abc',
        next_continuation_token = False
    )
    
    assert len(res.get('objects')) == 200

def test_if_filters_the_400_2022_files(pre_test):
    res = search_object.search_object(
        bucket = 'abc',
        prefix = 'abc',
        search_term = '2022',
        next_continuation_token = False
    )
    
    assert len(res.get('objects')) == 400

def test_if_filters_any_files(pre_test):
    res = search_object.search_object(
        bucket = 'abc',
        prefix = 'abc',
        search_term = 'zzz',
        next_continuation_token = False
    )
    
    assert len(res.get('objects')) == 0
