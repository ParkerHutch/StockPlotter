import pandas as pd

def process_data(dataset: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset in-place and add a percent change column for each day's
    change in stock price.

    Args:
        dataset (pd.DataFrame): a pandas DataFrame object representing the 
        raw data from the NASDAQ API

    Returns:
        pd.DataFrame: a DataFrame of the cleaned and processed data
    """

    clean_data(dataset)

    # Add daily % changes
    percent_change = lambda initial, final: 100.0 * (final - initial) / initial

    dataset['Percent Change'] = percent_change(
        dataset['Close/Last'].shift(1), dataset['Close/Last'].shift(0))
    

def clean_data(dataset: pd.DataFrame) -> pd.DataFrame:
    """Prepares the dataset in-place for processing. This step includes sorting
    the dataset by date, dropping the index, and cleaning column headers.

    Args:
        dataset (pd.DataFrame): a pandas DataFrame object representing the 
        raw data from the NASDAQ API

    """

    dataset.reset_index(drop=True, inplace=True)
    
    # Remove whitespaces in front of column names
    dataset.rename(lambda a: a.strip(), axis='columns', inplace=True)
    
    clean_price = lambda a: float(a.strip().replace('$', ''))
    
    # Remove $ symbols
    for price_column in ['Close/Last', 'Open', 'High', 'Low']:
        dataset[price_column] = dataset[price_column].map(clean_price)
    
    dataset['Date'] = pd.to_datetime(dataset['Date'])
    dataset.sort_values(by='Date', ascending=True, inplace=True)


def output_stock_info(ticker: str, dataset: pd.DataFrame):
    """Output useful information about the stock over the given time period to
    the console.

    Args:
        ticker (str): the stock ticker on the NASDAQ
        years_backward (float): the number of years analysis was conducted for
        dataset (pd.DataFrame): the pandas DataFrame containing stock info
    """

    print(f'{ticker} since {dataset["Date"].min().strftime("%b %Y")}:')
    
    max_percent_change_row = dataset.iloc[[dataset['Percent Change'].argmax()]]
    min_percent_change_row = dataset.iloc[[dataset['Percent Change'].argmin()]]     
    print(f'Max % Change: {max_percent_change_row["Percent Change"].item():.2f}%', 
        f'({max_percent_change_row["Date"].item().date().strftime("%m/%d/%Y")})')
    print(f'Min % Change: {min_percent_change_row["Percent Change"].item():.2f}%',
        f'({min_percent_change_row["Date"].item().date().strftime("%m/%d/%Y")})')
    max_price_row = dataset.iloc[[dataset['High'].argmax()]]
    print(f'High: ${max_price_row["High"].item():.2f}',
        f'({max_price_row["Date"].item().date().strftime("%m/%d/%Y")})')
    min_price_row = dataset.iloc[[dataset['Low'].argmin()]]
    print(f'Low: ${min_price_row["Low"].item():.2f}',
        f'({min_price_row["Date"].item().date().strftime("%m/%d/%Y")})')
    price_range = abs(max_price_row["High"].item() - 
                        min_price_row["Low"].item())
    print(f'Range: ${price_range:.2f}')