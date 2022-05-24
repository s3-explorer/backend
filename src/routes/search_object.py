import boto3
import pandas as pd
from flask import jsonify, request

from src.utils.constants import get_constants


def search_object():
    constants = get_constants()
    bucket = request.headers.get('x-bucket', False)
    prefix = request.headers.get('x-prefix', '')
    search_term = request.headers.get('x-search-term', '')
    next_continuation_token = request.headers.get(
        'x-next-continuation-token', False
    )

    if search_term == '':
        return 'Termo de busca inválido', 400
    if not bucket:
        return 'Bucket inválido', 400

    df_keys = pd.DataFrame()

    list_objects_config = {'Bucket': bucket, 'Prefix': prefix}
    while True:
        if next_continuation_token:
            list_objects_config['ContinuationToken'] = next_continuation_token

        s3_client = boto3.client(**constants.client_config)
        response = s3_client.list_objects_v2(**list_objects_config)
        keys = response.get('Contents', [])

        if len(keys) == 0:
            response_dict = {'next_continuation_token': False}
            response_dict['objects'] = []
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

        df_keys.loc[:, 'tmp_key'] = df_keys.loc[:, 'key'].str.replace(
            f'^{prefix}', '', regex=True
        )
        df_keys.loc[:, 'tmp_key'] = df_keys.loc[:, 'tmp_key'] + df_keys.loc[
            :, 'last_modified'
        ].dt.tz_localize(None).astype('str')
        df_keys = df_keys.loc[
            df_keys.loc[:, 'tmp_key']
            .str.lower()
            .str.contains(search_term.lower()),
            :,
        ].reset_index(drop=True)

        next_continuation_token = response.get('NextContinuationToken', False)
        if df_keys.shape[0] >= 50 or not next_continuation_token:
            break

    df_keys.loc[:, 'name'] = df_keys.loc[:, 'key'].str.split('/').str[-1]
    df_keys.loc[:, 'last_modified'] = df_keys.loc[
        :, 'last_modified'
    ].dt.tz_localize(None)
    df_keys.loc[:, 'name_lower'] = df_keys.loc[:, 'name'].str.lower()
    df_keys = df_keys.sort_values(
        by=['name_lower', 'last_modified'], ascending=[True, True]
    ).reset_index(drop=True)

    df_keys = df_keys.loc[:, ['name', 'last_modified', 'size', 'key']]
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
