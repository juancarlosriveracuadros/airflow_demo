

from astro.dataframes.pandas import DataFrame
from astro import sql as aql
from sklearn.datasets import fetch_california_housing
from sklearn.preprocessing import StandardScaler
import pandas as pd
from joblib import dump
from s3fs import S3FileSystem
from minio import Minio
from airflow.hooks.base import BaseHook
from io import BytesIO

#NAME_BUCKET = 'astro-ml'
#DATA_BUCKET = 'astro-ml/data'
#MODEL_BUCKET = 'astro-ml/model'

NAME_BUCKET = 'astro-ml'
DATA_BUCKET = 'astro-ml/housing/data'
MODEL_BUCKET = 'astro-ml/housing/model'

def _get_minio_client():
    minio = BaseHook.get_connection('minio')
    client = Minio(
        endpoint=minio.extra_dejson['endpoint_url'],
        access_key=minio.login,
        secret_key=minio.password,
        secure=False
    )
    return client

def _get_s3_client():
    minio = BaseHook.get_connection('minio_http')
    return S3FileSystem(
        key=minio.login,
        secret=minio.password,
        client_kwargs={
            'endpoint_url': minio.extra_dejson['endpoint_url']
        },
        use_ssl=False
    )


@aql.dataframe(task_id="extract")
def _extract_housing_data() -> DataFrame:
    from sklearn.datasets import fetch_california_housing
    return fetch_california_housing(download_if_missing=True, as_frame=True).frame


@aql.dataframe(task_id="featurize")
def _build_features(raw_df: DataFrame, model_dir: str) -> DataFrame:
    from sklearn.preprocessing import StandardScaler
    import pandas as pd
    from joblib import dump
    from s3fs import S3FileSystem

    client = _get_minio_client()

    if not client.bucket_exists(NAME_BUCKET):
        client.make_bucket(NAME_BUCKET)

    fs = _get_s3_client()

    target = "MedHouseVal"
    X = raw_df.drop(target, axis=1)
    y = raw_df[target]

    scaler = StandardScaler()
    X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    metrics_df = pd.DataFrame(scaler.mean_, index=X.columns)[0].to_dict()

    with fs.open(model_dir + "/scalar.joblib", "wb") as f:
        dump([metrics_df, scaler], f)

    X[target] = y

    return X

@aql.dataframe(task_id="train")
def _train_model(feature_df:DataFrame, model_dir: str) -> str:
    from sklearn.linear_model import RidgeCV
    import numpy as np
    from joblib import dump
    from s3fs import S3FileSystem


    fs = _get_s3_client()

    target = "MedHouseVal"


    model = RidgeCV(alphas=np.logspace(-3, 1, num=30))
    reg = model.fit(feature_df.drop(target, axis=1), feature_df[target])
    model_file_uri = model_dir + "/ridgecv.joblib"

    with fs.open(model_file_uri, "wb") as f:
        dump(reg, f)

    return model_file_uri

@aql.dataframe(task_id="predict")
def _predict_housing(feature_df: DataFrame, model_file_uri: str) -> DataFrame:
    from joblib import load

    fs = _get_s3_client()
    
    with fs.open(model_file_uri, "rb") as f:
        loaded_model = load(f)

    target = "MedHouseVal"
    feature_df['preds'] = loaded_model.predict(feature_df.drop(target, axis=1))

    return feature_df