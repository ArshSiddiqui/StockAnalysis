from pandas_datareader import data
import datetime
import pandas as pd
import colorama
from colorama import Fore
import matplotlib.pyplot as plt
import sys

def show_watchlist():
    today = datetime.date.today()
    yesterday = str(today - datetime.timedelta(14))
    end_date = str(today)

    print('Watchlist')
    print('Ticker   Price         Mvmt       % Mvmt')

    file = open('stocks.txt', 'r')
    lines = file.readlines()

    for line in lines:
        ticker = line.strip()
        panel_data = data.DataReader(ticker, 'yahoo', yesterday, end_date)
        proper_timeline_data = panel_data.iloc[-2:, :]
        close = proper_timeline_data['Close']

        difference = close[1] - close[0]
        percent_difference = close[1]/close[0]

        len_bw_tp = 9 - len(ticker)

        if difference < 0:
            print(Fore.RED + ticker, end="")
            for i in range(0, len_bw_tp):
                print(" ", end="")
            print('$' + str(close[1].round(2)) + '   ' + '\u25b2'
                  + '   ' + str(difference.round(2)) +
                  '      -' + str(percent_difference.round(2)) + '%')
        else:
            print(Fore.GREEN + ticker, end="")
            for i in range(0, len_bw_tp):
                print(" ", end="")
            print('$' + str(close[1].round(2)) + '   ' + '\u25bc'
            + '    +' + str(difference.round(2)) +
                  '      +' + str(percent_difference.round(2)) + '%' )


def add_stock(ticker):
    today = datetime.date.today()
    yesterday = str(today - datetime.timedelta(14))
    end_date = str(today)
    try:
        panel_data = data.DataReader(ticker, 'yahoo', yesterday, end_date)
    except:
        print("Try a different ticker")
        sys.exit(0)



    file = open('stocks.txt', 'a')
    file.write('\n' + ticker.upper())

if __name__ == "__main__":
    options = sys.argv[1:]
    if options[0] == 'watchlist':
        show_watchlist()
    elif options[0] == 'add':
        add_stock(options[1])