from sqlalchemy import create_engine, Table, Column, String, Float, Date, MetaData, select
from sqlalchemy.dialects.sqlite import insert
import datetime
import requests
from pprint import pprint
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"              
)

def fetch_data(url):
    logging.info("Fetching data from API")
    res=requests.get(url)   
    return res.json()

def _filter(data):
    logging.info("Filtering data")
    rates= data['rates']
    base=data['base']
    last_update=data['date']
    return rates, base, last_update


def load_data(rates, base, last_update):
    logging.info("Loading data into databse")
    engine=create_engine('sqlite:///currency.db',echo=False)
    meta=MetaData()

    exchange_rates=Table(
        'exchange_rates', meta,
        Column('currency', String, primary_key=True),
        Column('rate',Float),
        Column('base', String),
        Column('last_update', Date)
    )
    meta.create_all(engine)

    with engine.connect() as conn:
        for curr, rate in rates.items():
            dataset=insert(exchange_rates).values(
                currency=curr,
                rate=rate,
                base=base,
                last_update=datetime.datetime.strptime(last_update, '%Y-%m-%d').date()
            ).prefix_with("OR IGNORE")
            conn.execute(dataset)
            conn.commit()
    logging.info("Data loaded successfully")
if __name__=='__main__':
    url='https://api.exchangerate-api.com/v4/latest/usd'
    data=fetch_data(url)
    rates,base,last_update=_filter(data)
    load_data(rates, base, last_update)     