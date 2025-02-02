from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowNotFoundException
import requests
import json
from minio import Minio
from io import BytesIO
from datetime import datetime

BUCKET_NAME = 'stock-market'
now = datetime.now()

def _get_minio_client():
    minio = BaseHook.get_connection('minio')
    client = Minio(
        endpoint=minio.extra_dejson['endpoint_url'],
        access_key=minio.login,
        secret_key=minio.password,
        secure=False
    )
    return client

def _get_stock_prices(url, symbol):
    url = f"{url}{symbol}?metrics=high?&interval=1d&range=1y"
    api = BaseHook.get_connection('stock_api')
    response = requests.get(url, headers=api.extra_dejson['headers'])
    return  json.dumps(response.json()['chart']['result'][0])

def _store_prices(stock):
    client = _get_minio_client()
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)
    folder_path = f"input_prices/{now.strftime('%Y')}/{now.strftime('%m')}/{now.strftime('%d')}/{now.strftime('%H_%M')}"
    file_name = "prices.json"
    folder_path_latest = "input_prices/latest"
    stock = json.loads(stock)
    symbol = stock['meta']['symbol']
    data = json.dumps(stock, ensure_ascii=False).encode('utf8')
    
    objw = client.put_object(
        bucket_name=BUCKET_NAME,
        object_name=f'{symbol}/{folder_path}/{file_name}',
        data=BytesIO(data),
        length=len(data))
    
    objects = client.list_objects(BUCKET_NAME, prefix=f'{symbol}/{folder_path_latest}/')
    for obj in objects:
        client.remove_object(BUCKET_NAME, obj.object_name)

    objw = client.put_object(
        bucket_name=BUCKET_NAME,
        object_name=f'{symbol}/{folder_path_latest}/{file_name}',
        data=BytesIO(data),
        length=len(data))
    return f'{objw.bucket_name}/{symbol}/{folder_path}'

def _get_formatted_csv(path):
    _client = _get_minio_client()
    prefix_name = f"{path.split('/')[1]}/formatted_prices/latest/"
    objects = _client.list_objects(BUCKET_NAME, prefix=prefix_name, recursive=True)
    for obj in objects:
        if obj.object_name.endswith('.csv'):
            return obj.object_name
    raise AirflowNotFoundException(f"No CSV files found in {prefix_name}")