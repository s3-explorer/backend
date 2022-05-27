import boto3
import pandas as pd

from src.utils.constants import get_constants


def search_object(bucket, prefix, search_term, next_continuation_token):
    constants = get_constants()
    s3_client = boto3.client(**constants.client_config)

    df_keys, next_continuation_token = get_50_objects_or_more(
        s3_client, bucket, prefix, search_term, next_continuation_token
    )

    if df_keys.shape[0] == 0:
        return {'next_continuation_token': False, 'objects': []}

    df_keys = prepare_response(df_keys)

    return {
        'next_continuation_token': next_continuation_token,
        'objects': df_keys.to_dict('records'),
    }


def get_50_objects_or_more(
    s3_client, bucket, prefix, search_term, next_continuation_token
):
    list_objects_config = {'Bucket': bucket, 'Prefix': prefix}

    if next_continuation_token:
        list_objects_config[
            'next_continuation_token'
        ] = next_continuation_token

    df = pd.DataFrame()

    while True:
        response = s3_client.list_objects_v2(**list_objects_config)
        keys = response.get('Contents', [])

        if len(keys) == 0:
            return pd.DataFrame(), next_continuation_token

        df_keys = pd.DataFrame(keys)

        df_keys.loc[:, 'tmp_key'] = df_keys.loc[:, 'Key'].str.replace(
            f'^{prefix}', '', regex=True
        )

        df_keys.loc[:, 'tmp_key'] = df_keys.loc[:, 'tmp_key'] + df_keys.loc[
            :, 'LastModified'
        ].dt.tz_localize(None).astype('str')

        df_keys = df_keys.loc[
            df_keys.loc[:, 'tmp_key']
            .str.lower()
            .str.contains(search_term.lower()),
            :,
        ].reset_index(drop=True)

        df = pd.concat([df, df_keys], ignore_index=True)

        next_continuation_token = response.get('NextContinuationToken', False)
        if df_keys.shape[0] >= 50 or not next_continuation_token:
            break

    return (
        df.rename(
            columns={
                'Key': 'key',
                'LastModified': 'last_modified',
                'Size': 'size',
            }
        ),
        next_continuation_token,
    )


def prepare_response(df_keys):
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
    return df_keys
