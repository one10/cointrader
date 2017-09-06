#!/usr/bin/env python
import csv
from datetime import datetime, timedelta

WORKING_CAPITAL = 10000
COINBASE_FEE = 0.0199
# thanks, Kaggle: https://www.kaggle.com/mczielinski/bitcoin-historical-data
INPUT_FILENAME = './data/coinbaseUSD_1-min_data_1490188860_to_1496188800.csv'


def run_for_n_days(num_days, threshold_to_sell, print_short_stats=True, print_full_stats=False):
    dataset = {}
    max_timestamp = 0
    with open(INPUT_FILENAME, 'r', encoding="ascii") as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        next(datareader, None)  # skip the headers
        for row in datareader:
            dataset[int(row[0])] = float(row[1])
            max_timestamp = int(row[0])

    max_date = datetime.fromtimestamp(max_timestamp)
    min_date = max_date - timedelta(days=num_days)

    current_free_balance = WORKING_CAPITAL
    current_number_of_coins = 0
    last_purchase_price = -1
    last_historical_price = 0

    stats_buys = 0
    stats_sells = 0
    stats_curtick_num = 0

    for timestamp, price in dataset.items():
        if timestamp > min_date.timestamp():

            if current_number_of_coins > 0:
                assert last_purchase_price > -1

            # SELL rules
            # if coin price jumped more than THRESHOLD over last price, sell
            if current_number_of_coins > 0 and (
                        (price - last_purchase_price) / last_purchase_price) > threshold_to_sell:
                amount_made = current_number_of_coins * price
                fee = amount_made * COINBASE_FEE
                amount_made = amount_made - fee
                current_free_balance = current_free_balance + amount_made
                current_number_of_coins = 0
                stats_sells = stats_sells + 1

            # BUY rules
            # if don't have any coins and need to buy...
            if current_number_of_coins is 0:
                purchase_amt = WORKING_CAPITAL
                fee = purchase_amt * COINBASE_FEE
                purchase_amt_minus_fee = purchase_amt - fee
                current_number_of_coins = current_number_of_coins + purchase_amt_minus_fee / price
                last_purchase_price = price
                current_free_balance = current_free_balance - purchase_amt

                stats_buys = stats_buys + 1

                assert current_free_balance >= 0

            stats_curtick_num = stats_curtick_num + 1
            last_historical_price = price

    total_portfolio_value = current_number_of_coins * last_historical_price + current_free_balance

    if print_full_stats:
        print("***** Number of days: %d" % num_days)
        print("threshold_to_sell: %f" % threshold_to_sell)
        print("Ending current_free_balance: %f" % current_free_balance)
        print("Ending current_number_of_coins: %f" % current_number_of_coins)
        print("Ending value of current_number_of_coins: %f" % (current_number_of_coins * last_historical_price))
        print("Ending total in coin OR cash: %f" % total_portfolio_value)
        print("Ending stats_buys: %d" % stats_buys)
        print("Ending stats_sells: %d" % stats_sells)
        print("Ending stats_curtick_num: %d" % stats_curtick_num)

    if print_short_stats:
        print('%f, %f, %d' % (threshold_to_sell, total_portfolio_value, stats_sells))


if __name__ == '__main__':

    # try different thesholds
    for i in range(1, 51, 1):
        threshold = i / 10.0
        run_for_n_days(3000, threshold)
