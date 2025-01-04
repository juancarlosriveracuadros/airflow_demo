Overview
========

This project is a demo with two Data Pipelines as DAGs in Apache Airflow. The infrastructure of the project is base on Astronomer free version for localy deployment as base infrastructur and a docker-compose over ride file as well as a .env file for complementation purpose. In the justfile are some commands to rund and manage the project. For installation and implementation of justfile and astronomer "Astro-CLI" you will find the links at the end fo the README file in the documentation section.

Project Pipelines
================

## stock_market
In the file dags/stock_market.py you will find a DAG that is a ETL pipeline that download the API for Apple Inc.'s Stock Market Data (see documentation) into a minio bucket as json file. the Data will be transform in a csv file with a spark job. After the transformation the data will be save in the minio bucket and load into a postgres database table stock_market.

## astro mls 
A demo of a machine learning pipeline is represented in the file dags/astro_mls.py. the DAG download and prepare (Feature engineering) the data for the calculation of the model. The raw data as well as the prepared data will be save in the minio bucket. The model will be trained with the prepared data and the result will be save in the minio bucket. With the model a prediction will be made and the result will be save in the minio bucket and in the database table astro_ml.

Management the tool
=======================

## installation
for us this tool is necessary to have docker and the Astro-CLI installed on your machine. For install the Astro-CLI pleace see the documentation at the end of this README file. To manage the tool and fast installing ist recomended to install the justfile (see documentation as well). With the command "just init-airflow" you can install the services of the project. If there are some dificulties with the spark cluster pleace run the commands "just build-spark" and "just restart-airflow".

## justfile
for the management of the project you can use the justfile. The justfile is a file that contains a list of commands that can be executed with the just command.
to list the commands you can use the command "just" without any arguments or "just default".

## Access Services
access the following services over the browser:

### the airflow UI
- name: admin
- password: admin
- host-port: http://localhost:8080/

### the file system minio UI
- name: minio 
- password: minio123
- host-port: http://localhost:9000/

### access the database with the following credentials:
- host: localhost
- port: 5432
- user: postgres
- password: postgres
- database: postgres
with the command "just postgres" you can access the database over the terminal.

Documentation
===============
- Install astronmer "Astro-CLI": https://www.astronomer.io/docs/astro/cli/install-cli/
- justfile repository: https://github.com/casey/just
- API for Apple Inc.'s Stock Market Data: https://query1.finance.yahoo.com/v8/finance/chart/aapl?metrics=?&interval=1d&range=1y
- Orchentrator machine leaning: https://www.astronomer.io/docs/learn/use-case-airflow-ml-datasets/
