set ignore-comments
set positional-arguments


# Default command
# --------------

# Default recipe shows available commands
default:
    @just --list

# Airflow Core Commands
# -------------------

# Initialize new Airflow project and start services and connections
init-airflow:
    astro dev init
    just start-airflow

# Start Airflow services and configure connections
start-airflow:
    astro dev start
    just connections

# Stop Airflow services gracefully
stop-airflow:
    astro dev stop

# Force stop Airflow and clean networks
kill-airflow:
    astro dev kill
    docker network prune

# Restart all Airflow services
restart-airflow:
    astro dev restart

# Access Airflow container bash
start-bash:
    astro dev bash

# Connection Management
# -------------------

# Configure all required connections for the project
connections:
    # Yahoo Finance API connection
    -docker exec -it $(astro dev ps | grep scheduler | head -n 1 | awk '{print $1}') bash -c "airflow connections add 'stock_api' --conn-type 'http' --conn-host 'https://query1.finance.yahoo.com/' --conn-extra '{\"endpoint\": \"/v8/finance/chart/\",\"headers\": {\"Content-Type\": \"application/json\",\"User-Agent\": \"Morzilla/5.0\"}}'"
    # MinIO S3 connections
    -docker exec -it $(astro dev ps | grep scheduler | head -n 1 | awk '{print $1}') bash -c "airflow connections add 'minio' --conn-type 'aws' --conn-login 'minio' --conn-password 'minio123' --conn-extra '{\"endpoint_url\": \"minio:9000\"}'"
    -docker exec -it $(astro dev ps | grep scheduler | head -n 1 | awk '{print $1}') bash -c "airflow connections add 'minio_http' --conn-type 'aws' --conn-login 'minio' --conn-password 'minio123' --conn-extra '{\"endpoint_url\": \"http://minio:9000\"}'"
    # PostgreSQL connection
    -docker exec -it $(astro dev ps | grep scheduler | head -n 1 | awk '{print $1}') bash -c "airflow connections add 'postgres' --conn-type 'postgres' --conn-host 'postgres' --conn-login 'postgres' --conn-password 'postgres' --conn-port 5432"


# Database Management
# -----------------

# Connect to PostgreSQL database
postgres:
    #docker exec -it $(astro dev ps | grep postgres | head -n 1 | awk '{print $1}') psql -U postgres
    psql -h localhost -p 5432 -U postgres


# Spark Components
# --------------

# Build Spark application image
build-spark-app:
    docker build ./spark/notebooks/stock_transform -t airflow/stock-app


# Build Spark master node image
build-spark-master:
    docker build ./spark/master -t airflow/spark-master

# Build Spark worker node image
build-spark-worker:
    docker build ./spark/worker -t airflow/spark-worker


