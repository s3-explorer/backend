import re

import boto3
import pandas as pd
from flask import jsonify, request

from src.utils.constants import get_constants


def get_object_list():
    constants = get_constants()
    bucket = request.headers.get('x-bucket', False)
    prefix = request.headers.get('x-prefix', '')
    next_continuation_token = request.headers.get(
        'x-next-continuation-token', False
    )

    if prefix != '' and prefix[-1] != '/':
        return 'Prefixo inválido', 400
    if not bucket:
        return 'Bucket inválido', 400

    df_keys = pd.DataFrame()
    folders_list = []

    list_objects_config = {
        'Bucket': bucket,
        'Prefix': prefix,
        'Delimiter': '/',
    }

    s3_client = boto3.client(**constants.client_config)
    if next_continuation_token:
        list_objects_config['ContinuationToken'] = next_continuation_token
    else:
        paginator = s3_client.get_paginator('list_objects_v2')
        result = paginator.paginate(
            Bucket=bucket, Prefix=prefix, Delimiter='/'
        )
        for folder in result.search('CommonPrefixes'):
            if folder:
                folder_without_prefix = re.sub(
                    f'^{prefix}', '', folder.get('Prefix')
                )
                folders_list.append(
                    {
                        'name': folder_without_prefix.split('/')[0],
                        'is_folder': True,
                    }
                )

    response = s3_client.list_objects_v2(**list_objects_config)
    keys = response.get('Contents', [])

    if len(keys) == 0:
        response_dict = {'next_continuation_token': False}
        response_dict['objects'] = folders_list
        return jsonify(response_dict)

    df_keys = df_keys.append(
        pd.DataFrame(keys)
        .loc[:, ['Key', 'LastModified', 'Size']]
        .rename(
            columns={
                'Key': 'key',
                'LastModified': 'last_modified',
                'Size': 'size',
            }
        ),
        ignore_index=True,
    )

    next_continuation_token = response.get('NextContinuationToken', False)

    df_keys.loc[:, 'tmp_key'] = (
        df_keys.loc[:, 'key']
        .str.replace(f'^{prefix}', '', regex=True)
        .str.split('/')
    )
    df_keys.loc[:, 'name'] = df_keys.loc[:, 'tmp_key'].str[0]
    df_keys.loc[:, 'last_modified'] = df_keys.loc[
        :, 'last_modified'
    ].dt.tz_localize(None)
    df_keys.loc[:, 'is_folder'] = False
    if len(folders_list) > 0:
        df_keys = df_keys.append(pd.DataFrame(folders_list), ignore_index=True)
    df_keys.loc[:, 'name_lower'] = df_keys.loc[:, 'name'].str.lower()
    df_keys = df_keys.sort_values(
        by=['is_folder', 'name_lower', 'last_modified'],
        ascending=[False, True, True],
    ).reset_index(drop=True)

    df_keys = df_keys.loc[
        :, ['is_folder', 'name', 'last_modified', 'size', 'key']
    ]
    df_keys.fillna('', inplace=True)
    df_keys.loc[:, 'last_modified'] = df_keys.loc[:, 'last_modified'].astype(
        'str'
    )
    df_keys.loc[df_keys.loc[:, 'last_modified'] == 'NaT', 'last_modified'] = ''

    response_dict = {'next_continuation_token': next_continuation_token}
    response_dict['objects'] = df_keys.to_dict('records')
    del s3_client
    del df_keys

    return jsonify(response_dict)
