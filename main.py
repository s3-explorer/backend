import os

from flask import Flask
from flask_cors import CORS

from src.routes.download_object import download_object
from src.routes.get_buckets import get_buckets
from src.routes.get_object_list import get_object_list
from src.routes.search_object import search_object

app = Flask(__name__)
CORS(app)


@app.route('/api/get_buckets', methods=['GET'])
def route_get_buckets():
    try:
        return get_buckets()
    except Exception as e:
        print(e)
        return 'Oops! ocorreu um erro inesperado', 500


@app.route('/api/get_object_list', methods=['GET'])
def route_get_object_list():
    try:
        return get_object_list()
    except Exception as e:
        print(e)
        return 'Oops! ocorreu um erro inesperado', 500


@app.route('/api/download_object', methods=['GET'])
def route_download_object():
    try:
        return download_object()
    except Exception as e:
        print(e)
        return 'Oops! ocorreu um erro inesperado', 500


@app.route('/api/search_object', methods=['GET'])
def route_search_object():
    try:
        return search_object()
    except Exception as e:
        print(e)
        return 'Oops! ocorreu um erro inesperado', 500


if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(host='0.0.0.0', port=5000)
