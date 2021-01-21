import matplotlib.pyplot as plt
import seaborn as sns  # wrapper for numpy
from matplotlib.dates import DateFormatter

def plot_data(dataset, ticker):
    """ Plotting with Seaborn"""
    sns.set() # Set Seaborn style
    fig, ax = plt.subplots(facecolor='lightblue')
    ax.margins(x=0)
    date_form = DateFormatter('%b-%y')

    ax.xaxis.set_major_formatter(date_form)

    chart = sns.lineplot(x=dataset['Date'], y=dataset['Close/Last'], label=ticker)
    fig.tight_layout()

    plt.ylabel('Stock Price, USD ($)')
    date_range = [
        date.strftime('%B %Y') for date in [dataset['Date'].min().date(), 
                                                dataset['Date'].max().date()]]
    plt.title(f'{ticker} {date_range[0]} - {date_range[1]}')

    max_percent_change_row = dataset.iloc[[dataset['Percent Change'].idxmax()]]
    min_percent_change_row = dataset.iloc[[dataset['Percent Change'].idxmin()]] 

    plt.axvline(x=max_percent_change_row['Date'].item(), color='yellow', 
                linewidth=1, linestyle='dashdot', 
                label=f'{max_percent_change_row["Percent Change"].item():.2f}% Change')
    plt.axvline(x=min_percent_change_row['Date'].item(), color='orange', 
                linewidth=1, linestyle='dashdot', 
                label=f'{min_percent_change_row["Percent Change"].item():.2f}% Change') 

    max_price_row = dataset.iloc[[dataset['High'].idxmax()]]
    min_price_row = dataset.iloc[[dataset['Low'].idxmin()]] 

    plt.axvline(x=max_price_row['Date'].item(), color='green', linewidth=1, 
                linestyle='dashdot', 
                label=f'High (${max_price_row["High"].item():.2f})')
    plt.axvline(x=min_price_row['Date'].item(), color='red', linewidth=1, 
                linestyle='dashdot', 
                label=f'Low (${min_price_row["Low"].item():.2f})') 

    plt.legend()

    plt_fig = plt.gcf()
    plt.show()

    return plt_fig