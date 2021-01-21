import pandas as pd

def clean_data(raw_dataset):

    dataset = raw_dataset.iloc[::-1] # Reverse dataset so oldest value is at top
    dataset.reset_index(drop=True, inplace=True)

    # Remove whitespaces in front of column names
    dataset.rename(lambda a: a.strip(), axis='columns', inplace=True)
    
    clean_price = lambda a: float(a.strip().replace('$', ''))
    
    # Remove $ symbols
    for price_column in ['Close/Last', 'Open', 'High', 'Low']:
        dataset[price_column] = dataset[price_column].map(clean_price)
    
    dataset['Date'] = pd.to_datetime(dataset['Date'])

    return dataset


def process_data(raw_dataset):

    dataset = clean_data(raw_dataset)
    
    # Add daily % changes
    percent_change = lambda initial, final : 100.0 * (final - initial) / initial

    dataset['Percent Change'] = percent_change(
        dataset['Close/Last'].shift(1), dataset['Close/Last'].shift(0))
    
    return dataset


def output_stock_info(ticker, years_backward, dataset):
    """ Output stock info to console """ # TODO add formatting
    print(f'Some useful information for {ticker} over the last',
        f'{years_backward} years:')
    max_percent_change_row = dataset.iloc[[dataset['Percent Change'].idxmax()]]
    min_percent_change_row = dataset.iloc[[dataset['Percent Change'].idxmin()]]     
    print(f'Max % Change: {max_percent_change_row["Percent Change"].item():.2f}%', 
        f'({max_percent_change_row["Date"].item().date().strftime("%m/%d/%Y")})')
    print(f'Min % Change: {min_percent_change_row["Percent Change"].item():.2f}%',
        f'({min_percent_change_row["Date"].item().date().strftime("%m/%d/%Y")})')
    max_price_row = dataset.iloc[[dataset['High'].idxmax()]]
    print(f'High: ${max_price_row["High"].item():.2f}',
        f'({max_price_row["Date"].item().date().strftime("%m/%d/%Y")})')
    min_price_row = dataset.iloc[[dataset['Low'].idxmin()]]
    print(f'Low: ${min_price_row["Low"].item():.2f}',
        f'({min_price_row["Date"].item().date().strftime("%m/%d/%Y")})')
    price_range = abs(max_price_row["High"].item() - 
                        min_price_row["Low"].item())
    print(f'Range: ${price_range:.2f}')