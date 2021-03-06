from typing import Tuple
from helpers import analyzer, retriever, plotter

def get_user_input() -> Tuple[str, float]:
    """Ask the user for a ticker and the number of years backward to go, then
    return the user's answers.

    Returns:
        Tuple[str, float]: the ticker and number of years backward to go
    """

    ticker = input('Ticker: ').upper()
    years_backward = float(input("Years back: ")) # TODO accept float input

    return ticker, years_backward


def main():
    
    ticker, years_backward = get_user_input()
    while (dataset := retriever.get_data(ticker, years_backward)) is None:
        print("That ticker/time combo didn't work, please enter a new one.")
        ticker, years_backward = get_user_input()
    
    analyzer.process_data(dataset)

    analyzer.output_stock_info(ticker, dataset)

    plt_fig = plotter.plot_data(dataset, ticker)

    plt_fig.savefig('./output/plot.png', bbox_inches='tight')

    dataset.to_csv(path_or_buf='./output/data.csv', index=False)


if __name__ == '__main__':
    main()
