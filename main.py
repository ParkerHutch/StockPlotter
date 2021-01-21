"""
Retrieves an online dataset for a user-specified stock and timeframe, then
plots that stock's closing price over that timeframe
"""

import analyzer
import retriever
import plotter

def get_user_input():
    """Ask the user for a ticker and the number of years backward to go, then
    return the user's answers.

    Returns:
        Tuple[str, int]: the ticker and number of years backward to go
    """
    ticker = input('Ticker: ').upper()
    years_backward = int(input("Years back: ")) # TODO accept float input

    return ticker, years_backward


def main():
    
    ticker, years_backward = get_user_input()
    while (raw_data := retriever.get_data(ticker, years_backward)) is None:
        print("That ticker/time combo didn't work, please enter a new one.")
        ticker, years_backward = get_user_input()
    
    dataset = analyzer.process_data(raw_data)

    analyzer.output_stock_info(ticker, years_backward, dataset)

    plt_fig = plotter.plot_data(dataset, ticker)

    plt_fig.savefig('plot.png', bbox_inches='tight')

    dataset.to_csv(path_or_buf='./data.csv', index=False)


if __name__ == '__main__':
    main()
