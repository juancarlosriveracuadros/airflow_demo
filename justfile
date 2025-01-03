set ignore-comments
set positional-arguments

init-airflow:
    astro dev init
    just start-airflow
    just connections

start-airflow:
    astro dev start
    just connections

stop-airflow:
    astro dev stop

kill-airflow:
    astro dev kill
    docker network prune

restart-airflow:
    astro dev restart

start-bash:
    astro dev bash

connections:
    -docker exec -it $(astro dev ps | grep scheduler | head -n 1 | awk '{print $1}') bash -c "airflow connections add 'stock_api' --conn-type 'http' --conn-host 'https://query1.finance.yahoo.com/' --conn-extra '{\"endpoint\": \"/v8/finance/chart/\",\"headers\": {\"Content-Type\": \"application/json\",\"User-Agent\": \"Morzilla/5.0\"}}'"
    -docker exec -it $(astro dev ps | grep scheduler | head -n 1 | awk '{print $1}') bash -c "airflow connections add 'minio' --conn-type 'aws' --conn-login 'minio' --conn-password 'minio123' --conn-extra '{\"endpoint_url\": \"minio:9000\"}'"
    -docker exec -it $(astro dev ps | grep scheduler | head -n 1 | awk '{print $1}') bash -c "airflow connections add 'minio_http' --conn-type 'aws' --conn-login 'minio' --conn-password 'minio123' --conn-extra '{\"endpoint_url\": \"http://minio:9000\"}'"
    -docker exec -it $(astro dev ps | grep scheduler | head -n 1 | awk '{print $1}') bash -c "airflow connections add 'postgres' --conn-type 'postgres' --conn-host 'postgres' --conn-login 'postgres' --conn-password 'postgres' --conn-port 5432"


postgres:
    docker exec -it $(astro dev ps | grep postgres | head -n 1 | awk '{print $1}') psql -U postgres
    #psql -h localhost -p 5432 -U postgres



build-spark-app:
    docker build ./spark/notebooks/stock_transform -t airflow/stock-app

build-spark-master:
    docker build ./spark/master -t airflow/spark-master

build-spark-worker:
    docker build ./spark/worker -t airflow/spark-worker