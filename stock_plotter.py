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
    dataset['Percent Change'][0] = 0 # TODO should probably be N/A
    
    # Add year column
    dataset.reset_index(drop=True)

    dataset['Year'] = dataset['Date'].str.split('/', expand=True)[2]
    
    return dataset

def get_largest_percent_change_rows(dataset):
    max_percent_change_index = dataset['Percent Change'].idxmax()
    min_percent_change_index = dataset['Percent Change'].idxmin()
    max_percent_change_row = dataset.iloc[[max_percent_change_index]]
    min_percent_change_row = dataset.iloc[[min_percent_change_index]]
    return max_percent_change_row, min_percent_change_row

def get_max_price_row(dataset):
    return dataset.iloc[[dataset['High'].idxmax()]]

def get_min_price_row(dataset):
    return dataset.iloc[[dataset['Low'].idxmin()]]

""" Get user input """
ticker = input('Ticker: ')
years_backward = int(input("Years back: ")) # TODO accept float input
while not is_valid_start_date(ticker, years_backward): # TODO use datetime module to get day a year ago
    ticker = input("That didn't work, please enter a new ticker:")
    years_backward = int(input("That didn't work, please enter another year amount:"))
   
dataset = get_dataset(ticker, years_backward)

today = datetime.now()

""" Output stock info to console """ # TODO add formatting
print(f'Some useful information for {ticker} over the last {years_backward} years:')
max_percent_change_row, min_percent_change_row = get_largest_percent_change_rows(dataset)
print(f'Max % Change: {max_percent_change_row["Percent Change"].item():.2f}% ({max_percent_change_row["Date"].item()})')
print(f'Min % Change: {min_percent_change_row["Percent Change"].item():.2f}% ({min_percent_change_row["Date"].item()})')
max_price_row = get_max_price_row(dataset)
print(f'High: ${max_price_row["High"].item():.2f} ({max_price_row["Date"].item()})')
min_price_row = get_min_price_row(dataset)
print(f'Low: ${min_price_row["Low"].item():.2f} ({min_price_row["Date"].item()})')
price_range = abs(max_price_row["High"].item() - min_price_row["Low"].item())
print(f'Range: ${price_range:.2f}')

dataset['Date'] = pd.to_datetime(dataset['Date']) # NOTE not tested for effects


# TODO: put a point where the largest % change occurs
# TODO: add title: $TICKER startDate - endDate
""" Plotting with Seaborn"""
sns.set() # Set Seaborn style
fig, ax = plt.subplots(facecolor='lightblue')
ax.margins(x=0)
#plt.fill_between(dataset.index, dataset['Close/Last'])
from matplotlib.dates import DateFormatter
date_form = DateFormatter('%m-%y')

ax.xaxis.set_major_formatter(date_form)

chart = sns.lineplot(x=dataset['Date'],
                     y=dataset['Close/Last'], 
                     label=ticker)
fig.tight_layout()

plt.ylabel('Stock Price($)')
plt.legend([ticker]) # TODO include axvline labels
dataset['Date'] = pd.to_datetime(dataset['Date']) # TODO would this fix weird plotting year thing?
dates = [date.strftime('%m/%d/%Y') for date in [dataset['Date'].min().date(), dataset['Date'].max().date()]]
plt.title(f'${ticker} {dates[0]}-{dates[1]}')

max_percent_change_row = dataset.iloc[[dataset['Percent Change'].idxmax()]] 
min_percent_change_row = dataset.iloc[[dataset['Percent Change'].idxmin()]] 

plt.axvline(x=max_percent_change_row['Date'].item(), color='yellow', linewidth=1, linestyle='dashdot', label='Maximum % Change') # TODO use label on legend
plt.axvline(x=min_percent_change_row['Date'].item(), color='orange', linewidth=1, linestyle='dashdot', label='Minimum % Change') 

max_price_row = get_max_price_row(dataset)
min_price_row = get_min_price_row(dataset)

plt.axvline(x=max_price_row['Date'].item(), color='green', linewidth=1, linestyle='dashdot', label='High') # TODO use label on legend
plt.axvline(x=min_price_row['Date'].item(), color='red', linewidth=1, linestyle='dashdot', label='Low') 

plt.legend()

plt_fig = plt.gcf()
plt.show()
while (answer := input('Save figure to file? (Y/N):').upper()) not in ['Y', 'N']:
    print('Please enter Y or N.')
if answer == 'Y':
    plt_fig.savefig('plot.png', bbox_inches='tight')

while (answer := input('Save dataset to file? (Y/N):').upper()) not in ['Y', 'N']:
    print('Please enter Y or N.')
if answer == 'Y':
    print('here')
    print(dataset)
    dataset.to_csv(path_or_buf='./data.csv', index=False)