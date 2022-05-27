from datetime import datetime
from random import randint


object_with_abc_abc_x = [
    {
        'Key': f'abc/abc_{i}.txt',
        'LastModified': datetime.strptime(f'2022-{str(randint(1,12)).zfill(2)}-{str(randint(1,28)).zfill(2)}', '%Y-%m-%d'),
        'Size': randint(44,78924),
    } 
    for i in range(0,5)
]

object_with_abc_xyz_x = [
    {
        'Key': f'abc/xyz_{i}.txt',
        'LastModified': datetime.strptime(f'2022-{str(randint(1,12)).zfill(2)}-{str(randint(1,28)).zfill(2)}', '%Y-%m-%d'),
        'Size': randint(44,78924),
    } 
    for i in range(0,5)
]

object_with_xyz_abc_x = [
    {
        'Key': f'xyz/abc_{i}.txt',
        'LastModified': datetime.strptime(f'2022-{str(randint(1,12)).zfill(2)}-{str(randint(1,28)).zfill(2)}', '%Y-%m-%d'),
        'Size': randint(44,78924),
    } 
    for i in range(0,5)
]

object_with_xyz_xyz_x = [
    {
        'Key': f'xyz/xyz_{i}.txt',
        'LastModified': datetime.strptime(f'2022-{str(randint(1,12)).zfill(2)}-{str(randint(1,28)).zfill(2)}', '%Y-%m-%d'),
        'Size': randint(44,78924),
    } 
    for i in range(0,5)
]

class mock_s3_client:
    def __init__(self, *args, **kwargs) -> None:
        ...

    def list_objects_v2(self, *args, **kwargs):
        prefix = kwargs.get('Prefix', '')

        data = []
        if prefix == '':
            data = object_with_abc_abc_x + object_with_abc_xyz_x + object_with_xyz_abc_x + object_with_xyz_xyz_x
        elif prefix == 'abc':
            data = object_with_abc_abc_x + object_with_abc_xyz_x
        elif prefix == 'xyz':
            data = object_with_xyz_abc_x + object_with_xyz_xyz_x

        return {
            'Contents': data
        }
