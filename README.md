# Data Pipeline Demo with Apache Airflow

## Table of Contents
- [Overview](#overview)
- [Data Pipelines](#data-pipelines)
  - [Stock Market Pipeline](#stock-market-pipeline)
  - [Machine Learning Pipeline](#machine-learning-pipeline)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Quick Start](#quick-start)
- [Service Access](#service-access)
  - [Airflow Web Interface](#airflow-web-interface)
  - [MinIO Object Storage](#minio-object-storage)
  - [PostgreSQL Database](#postgresql-database)
- [Known Issues](#Issues)
- [Documentation](#documentation)

## Overview

This project demonstrates two Data Pipelines implemented as DAGs (Directed Acyclic Graphs) in Apache Airflow. The infrastructure leverages Astronomer's free version for local deployment, utilizing Docker Compose and environment configurations for extended functionality. Project management is streamlined through a comprehensive justfile containing essential commands for deployment and maintenance.

## Data Pipelines

### Stock Market Pipeline
Located in `dags/stock_market.py`, this ETL pipeline:
- Fetches Apple Inc.'s Stock Market Data via API
- Stores raw data in MinIO as JSON
- Transforms data using Spark jobs into CSV format
- Loads processed data into PostgreSQL table `stock_market` and MinIO bucket.

### Machine Learning Pipeline
Located in `dags/astro_mls.py`, this ML pipeline:
- Downloads and performs feature engineering on raw data
- Stores both raw and prepared datasets in MinIO
- Trains ML models using prepared data
- Generates predictions and stores results in:
  - MinIO bucket
  - PostgreSQL table `astro_ml`


## Setup and Installation

### Prerequisites
- Docker
- Astro CLI
- Just command runner

### Quick Start
1. Install Astro CLI (see documentation links)
2. Install Just command runner
3. Initialize services with the command "just init-airflow"

## Issues
- For spark cluster issues execute:
    - update-spark


## Service Access

### Airflow Web Interface
- name: admin
- password: admin
- URL: http://localhost:8080/

### MinIO Object Storage
- name: minio 
- password: minio123
- URL: http://localhost:9000/

### PostgreSQL Database
- host: localhost
- port: 5432
- user: postgres
- password: postgres
- database: postgres
access via terminal "just postgres"

# Documentation
- [Astro CLI Installation Guide](https://www.astronomer.io/docs/astro/cli/install-cli/)
- [Just Command Runner](https://github.com/casey/just)
- [Yahoo Finance API](https://query1.finance.yahoo.com/v8/finance/chart/aapl?metrics=?&interval=1d&range=1y)
- [Airflow ML Orchestration Guide](https://www.astronomer.io/docs/learn/use-case-airflow-ml-datasets/)
