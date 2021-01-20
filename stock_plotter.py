"""
Retrieves an online dataset for a user-specified stock and timeframe, then
plots that stock's closing price over that timeframe
"""

import io
import time
import urllib
import warnings
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns  # wrapper for numpy

warnings.filterwarnings('ignore') # TODO remove?

def construct_nasdaq_url(ticker, years_backward):
    today = datetime.date(datetime.now())
    
    start_date = today - timedelta(days = years_backward * 365) 
    return 'https://www.nasdaq.com/api/v1/historical/{}/stocks/{}/{}'.format(ticker, start_date, today)

"""
def construct_nasdaq_url(ticker, start_date, end_date):
    return 'https://www.nasdaq.com/api/v1/historical/{}/stocks/{}/{}'.format(ticker, start_date, end_date)
"""

def retrieve_data(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'My User Agent 1.0') 
    req.add_header('From', 'youremail@domain.com') # TODO not sure if needed
    response = urllib.request.urlopen(req)
    if response.length is not None and response.length <= 1:
        print("Couldn't retrieve dataset with that URL:", url)
        return None
    else:
        data = response.read().decode('utf-8')
        return pd.read_csv(io.StringIO(data))
    
def calculate_percent_increase(initial, final):
    return 100.0 * (final - initial) / initial


def is_valid_start_date(ticker, years_backward):
    data = retrieve_data(construct_nasdaq_url(ticker, years_backward))
    if data is not None:
        return True
    else:
        return False
    
def get_dataset(ticker, years_backward):

    dataset = retrieve_data(construct_nasdaq_url(ticker, years_backward))
    
    dataset = dataset.iloc[::-1] # Reverse dataset so oldest value is at top
    dataset.reset_index(drop=True, inplace=True)
    
    # Remove whitespaces in front of column names
    dataset.rename(lambda a: a.strip(), axis='columns', inplace=True)
    
    clean_price = lambda a: float(a.strip().replace('$', ''))
    
    # Cleaning Data: remove $ symbols
    for price_column in ['Close/Last', 'Open', 'High', 'Low']:
        dataset[price_column] = dataset[price_column].map(clean_price)
    
    # Add daily % changes
    
    dataset['Percent Change'] = calculate_percent_increase(
        dataset['Close/Last'].shift(1), dataset['Close/Last'].shift(0))
    dataset['Percent Change'][0] = 0 
    
    # Add year column
    dataset.reset_index(drop=True)

    dataset['Year'] = dataset['Date'].str.split('/', expand=True)[2]
    
    return dataset

""" Get user input """
ticker = input('Ticker:')
years_backward = int(input("Years back: "))
while not is_valid_start_date(ticker, years_backward):
    ticker = input("That didn't work, please enter a new ticker:")
    years_backward = int(input("That didn't work, please enter another year amount:"))
   
dataset = get_dataset(ticker, years_backward)

today = datetime.now()

""" Plotting with Seaborn"""
sns.set() # Set Seaborn style
fig, ax = plt.subplots(facecolor='lightblue')
ax.margins(x=0)
#plt.fill_between(dataset.index, dataset['Close/Last'])
chart = sns.lineplot(x=dataset.index / 365 + int(today.year - years_backward), 
                     y=dataset['Close/Last'], legend='full')
fig.tight_layout()
plt.ylabel('Stock Price($)')
plt.legend([ticker])

plt_fig = plt.gcf()
plt.show()
while (answer := input('Save figure to file? (Y/N):').upper()) not in ['Y', 'N']:
    print('Please enter Y or N.')
if answer == 'Y':
    plt_fig.savefig('plot.png', bbox_inches='tight')
