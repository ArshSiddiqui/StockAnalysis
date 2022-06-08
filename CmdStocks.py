from pandas_datareader import data
import datetime
import pandas as pd
import colorama
from colorama import Fore
import matplotlib.pyplot as plt
import sys
import termplotlib as tpl

def show_watchlist():
    today = datetime.date.today()
    yesterday = str(today - datetime.timedelta(14))
    end_date = str(today)

    print('Watchlist')
    print('Ticker   Price          Mvmt       % Mvmt')

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
        len_bw_pm = 10 - len(str(close[1].round(2)))

        if difference < 0:
            print(Fore.RED + ticker, end="")
            for i in range(0, len_bw_tp):
                print(" ", end="")
            print('$' + str(close[1].round(2)), end="")
            for i in range(0, len_bw_pm):
                print(" ", end="")
            print('\u25b2' + '   ' + str(difference.round(2)) +
                  '      -' + str(percent_difference.round(2)) + '%')
        else:
            print(Fore.GREEN + ticker, end="")
            for i in range(0, len_bw_tp):
                print(" ", end="")
            print('$' + str(close[1].round(2)), end="")
            for i in range(0, len_bw_pm):
                print(" ", end="")
            print('\u25b2' + '   +' + str(difference.round(2)) +
                  '      +' + str(percent_difference.round(2)) + '%')


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


def remove_stock(ticker):
    file = open('stocks.txt', 'r')
    lines = file.readlines()
    file.close()

    new_file = open('stocks.txt', 'w')
    spot = 0
    for line in lines:
        if line.strip('\n') != ticker.upper():
            if spot != 0:
                new_file.write('\n')
            new_file.write(line.strip('\n'))
            spot += 1

    new_file.close()


def graph(ticker):
    today = datetime.date.today()
    yesterday = str(today - datetime.timedelta(7))
    end_date = str(today)
    panel_data = data.DataReader(ticker.upper(), 'yahoo', yesterday, end_date)
    close = panel_data['Close']

    all_weekdays = pd.date_range(start=yesterday, end=end_date, freq='B')
    close = close.reindex(all_weekdays)
    close = close.fillna(method='ffill')

    fig = tpl.figure()
    x = [1, 2, 3, 4, 5, 6]
    fig.plot(x, close.tolist(), label=ticker.upper(), width=80, height=20)
    fig.show()


if __name__ == "__main__":
    options = sys.argv[1:]
    if options[0] == 'watchlist':
        show_watchlist()
    elif options[0] == 'add':
        add_stock(options[1])
    elif options[0] == 'rm':
        remove_stock(options[1])
    elif options[0] == 'graph':
        graph(options[1])