from datetime import datetime
from airflow.decorators import dag
import os
from astro import sql as aql
from astro.files import File
from astro.dataframes.pandas import DataFrame
from astro.sql.table import Table, Metadata

from include.astro_ml.tasks import _extract_housing_data, _build_features, _train_model, _predict_housing,MODEL_BUCKET, DATA_BUCKET 

@dag(
    schedule='@daily', 
    start_date=datetime(2024, 1, 1), 
    catchup=False,
    tags=['astro_ml']
)

def astro_ml():
    model_id = datetime.utcnow().strftime("%y_%d_%m_%H_%M_%S_%f")
    model_dir = os.path.join(MODEL_BUCKET, model_id)


    extract_df = _extract_housing_data()

    loaded_data = aql.export_file(
        task_id='save_data',
        input_data=extract_df,
        output_file=File(
            path=f's3://{DATA_BUCKET}/housing.csv',
            conn_id='minio_http'
                         ),
        if_exists='replace')
    
    feature_df = _build_features(extract_df, model_dir)

    model_file_uri = _train_model(feature_df, model_dir)

    pred_df = _predict_housing(feature_df, model_file_uri)

    pred_file = aql.export_file(
        task_id="save_predictions",
        input_data=pred_df,
        output_file=File(
            path=f's3://{DATA_BUCKET}/housing_pred.csv',
            conn_id='minio_http'
            ),
        if_exists="replace")

    load_to_dw = aql.load_file(
        task_id='load_to_dw',
        input_file=File(
            path=f's3://{DATA_BUCKET}/housing_pred.csv',
            conn_id='minio_http'),
        output_table=Table(
            name='astro_ml',
            conn_id='postgres',            
            metadata=Metadata(schema='public')
        )
    )

    pred_file >> load_to_dw
astro_ml()