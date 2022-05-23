from email import header
from wsgiref import headers
from main import app

def test_if_test_content_have_20_files():
    client = app.test_client()

    response = client.get("/api/search_object", headers={
        'x-bucket': 'mybucket-1',
        'x-search-term': 'file'
    })

    assert len(response.json['objects']) == 20