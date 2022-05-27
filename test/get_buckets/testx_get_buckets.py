from main import app

def test_if_all_buckets_will_be_return():
    """Verificar se todos os buckets criados serão retornados sem passar nenhuma restrição do que mostrar ou não"""
    client = app.test_client()
    res = client.get('/api/get_buckets')

    assert res.json == ["mybucket-1", "mybucket-2"]

