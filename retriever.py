import io
import urllib
from datetime import datetime, timedelta

import pandas as pd  # used to read response as csv

def get_data(ticker, years_backward):
    url = get_nasdaq_endpoint(ticker, years_backward)
    data = request_data(url)
    return data


def get_nasdaq_endpoint(ticker, years_backward):
    today = datetime.date(datetime.now())
    
    start_date = today - timedelta(days = years_backward * 365) 
    return f'https://www.nasdaq.com/api/v1/historical/{ticker}/stocks/{start_date}/{today}'


def request_data(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'My User Agent 1.0') 
    response = urllib.request.urlopen(req)
    if response.length is not None and response.length <= 1:
        return None
    else:
        data = response.read().decode('utf-8')
        return pd.read_csv(io.StringIO(data))


def url_has_data(url):
    data = request_data(url)
    if data is not None:
        return True
    else:
        return False
