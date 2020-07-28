import os
import time
import json
import logging
from datetime import datetime, timedelta
from selenium import webdriver
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.latest_only_operator import LatestOnlyOperator
import pycurl
import requests
import json
from selenium.webdriver.chrome.options import Options
from crawl import RunCrawl
from datetime import date
from glob import glob
import pandas as pd
import ntpath

default_args = {
    'owner': 'AndySu',
    'start_date': datetime(2020, 7, 26, 9, 5),
    'schedule_interval': '@daily',
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

def get_slack_url():
    file_dir = os.path.dirname(__file__)
    json_path = os.path.join(file_dir, '../data/slack.json')
    with open(json_path, 'r') as fp:
        url = json.load(fp)['url']
        return url

def get_stock_history(**context):
    RunCrawl()

def readCsv(path):
    df = pd.read_csv(path)
    num = ntpath.basename(path)[:-3]

    return '股票代碼: ' + num +' 價格:' + str(df.values[0][1]) + '\n'

def get_message_text():
    file_dir = os.path.dirname(__file__)
    message_path = os.path.join(file_dir, '../data')
    files_dir = '{}/{}/{}'.format(message_path, date.today().strftime('%Y%m%d'), '*')
    filesList = glob(files_dir)
    
    message = ""
    for path in filesList:
        message += readCsv(path)

    return message

def send_notification(**context):
    send_msg(get_message_text())
    return 

def send_msg(msg):
    # HTTP POST Request
    s_url = get_slack_url()

    dict_headers = {'Content-type': 'application/json'}

    dict_payload = {
        "text": msg}
    json_payload = json.dumps(dict_payload)

    rtn = requests.post(s_url, data=json_payload, headers=dict_headers)
    print(rtn.text)

with DAG('stock_app', default_args=default_args) as dag:

    # define tasks
    latest_only = LatestOnlyOperator(task_id='latest_only')

    get_stock_history = PythonOperator(
        task_id='get_stock_history',
        python_callable=get_stock_history,
        provide_context=True
    )

    send_notification = PythonOperator(
        task_id='send_notification',
        python_callable=send_notification,
        provide_context=True
    )

    # define workflow
    latest_only >> get_stock_history
    get_stock_history >> send_notification
