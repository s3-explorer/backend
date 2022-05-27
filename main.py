import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from src.routes.download_object import download_object
from src.routes.get_buckets import get_buckets
from src.routes.get_object_list import get_object_list
from src.routes.search_object import search_object

app = Flask(__name__)
CORS(app)

DEFAULT_ERROR_RESPONSE = 'Oops! ocorreu um erro inesperado'


@app.route('/api/get_buckets', methods=['GET'])
def route_get_buckets():
    try:
        return jsonify(get_buckets())
    except Exception as e:
        print(e)
        return DEFAULT_ERROR_RESPONSE, 500


@app.route('/api/get_object_list', methods=['GET'])
def route_get_object_list():
    try:
        return get_object_list()
    except Exception as e:
        print(e)
        return DEFAULT_ERROR_RESPONSE, 500


@app.route('/api/download_object', methods=['GET'])
def route_download_object():
    try:
        return download_object()
    except Exception as e:
        print(e)
        return DEFAULT_ERROR_RESPONSE, 500


@app.route('/api/search_object', methods=['GET'])
def route_search_object():
    try:
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

        return jsonify(
            search_object(bucket, prefix, search_term, next_continuation_token)
        )
    except Exception as e:
        print(e)
        return DEFAULT_ERROR_RESPONSE, 500


if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(host='0.0.0.0', port=5000)
