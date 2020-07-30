# StockCrawlerSendSlack

## Install 
```bash
pip install "apache-airflow[crypto, slack]"
```

## Run
```bash
git clone https://github.com/a07458666/StockCrawlerSendSlack.git
cd StockCrawlerSendSlack
export AIRFLOW_HOME="$(pwd)"
airflow initdb
airflow webserver -p 8080
airflow scheduler
```

## Demo
![image](https://github.com/a07458666/StockCrawlerSendSlack/blob/master/demo/demo.PNG)
