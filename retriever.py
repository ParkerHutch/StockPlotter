import io
import urllib
from datetime import datetime, timedelta

import pandas as pd

def get_data(ticker:str, years_backward:float) -> pd.DataFrame:
    """Attempt to return NASDAQ data as a pandas DataFrame object for the given
    stock ticker, going back the given number of years. If the ticker or
    timeframe is invalid, None will be returned. 

    Args:
        ticker (str): the stock ticker on the NASDAQ
        years_backward (int): the number of years backward to go

    Returns:
        pandas.DataFrame: a DataFrame of the NASDAQ data for the given stock
        ticker over the last years_backward_years, or None if no data was found
    """
    
    url = get_nasdaq_endpoint(ticker, years_backward)
    data = request_data(url)
    return data


def get_nasdaq_endpoint(ticker: str, years_backward: float) -> str:
    """Construct a NASDAQ API url that pertains to the given stock ticker, going
    back the given number of years.

    Args:
        ticker (str): the stock ticker on the NASDAQ
        years_backward (int): the number of years back to go

    Returns:
        str: the NASDAQ API url, which, if valid, should return a dataset file 
        as a CSV when accessed with a GET request
    """

    today = datetime.date(datetime.now())
    
    start_date = today - timedelta(days = years_backward * 365) 
    return f'https://www.nasdaq.com/api/v1/historical/{ticker}/stocks/{start_date}/{today}'


def request_data(url:str) -> pd.DataFrame:
    """Make a GET request to the given URL, returning the response data as a
    pandas DataFrame if data is found and None if otherwise. This function
    expects the response from the URL to be a CSV file.

    Args: 
        url (str): the url to access with a GET request

    Returns: 
        pandas.DataFrame: a DataFrame of the url's CSV file response if it was
        given, None otherwise
    """

    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'My User Agent 1.0') 
    response = urllib.request.urlopen(req)
    if response.length is not None and response.length <= 1:
        return None
    else:
        data = response.read().decode('utf-8')
        return pd.read_csv(io.StringIO(data))