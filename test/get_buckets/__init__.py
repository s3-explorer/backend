class mock_s3_client:
    def __init__(self, *args, **kwargs) -> None:
        ...

    def list_buckets(self, *args, **kwargs):
        return {
            'Buckets': [
                {'Name': 'my-bkt-01'},
                {'Name': 'my-bkt-02'},
                {'Name': 'my-bkt-03'},
                {'Name': 'my-bkt-04'},
            ]
        }