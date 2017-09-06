#!/usr/bin/env python
import csv
from datetime import datetime, timedelta

WORKING_CAPITAL = 10000
COINBASE_FEE = 0.0199
# thanks, Kaggle: https://www.kaggle.com/mczielinski/bitcoin-historical-data
INPUT_FILENAME = './data/coinbaseUSD_1-min_data_1490188860_to_1496188800.csv'


class CoinTrader:
    def read_file(self, input_filename, num_days):
        with open(input_filename, 'r', encoding="ascii") as csvfile:
            datareader = csv.reader(csvfile, delimiter=',')
            self.load_data(datareader, num_days)

    def read_data(self, input_data, num_days):
        self.load_data(csv.reader(input_data), num_days, False)

    def load_data(self, datareader, num_days, skip_header=True):
        self.dataset = []
        max_timestamp = 0
        if skip_header:
            next(datareader, None)
        for row in datareader:
            self.dataset.append((int(row[0]), float(row[1])))
            max_timestamp = int(row[0])

        self.start_dt = datetime.fromtimestamp(max_timestamp)
        self.start_dt = datetime.fromtimestamp(max_timestamp) - timedelta(days=num_days)
        assert len(self.dataset) > 0

    def run(self, threshold_to_sell, print_short_stats=False, print_full_stats=False):
        current_cash_balance = WORKING_CAPITAL
        current_number_of_coins = 0
        last_purchase_price = -1
        last_historical_price = 0

        stats_buys = 0
        stats_sells = 0
        stats_curtick_num = 0

        for (timestamp, price) in self.dataset:
            if timestamp >= self.start_dt.timestamp():

                if current_number_of_coins > 0:
                    assert last_purchase_price > -1

                # SELL rules
                # if coin price jumped more than THRESHOLD over last price, sell
                if current_number_of_coins > 0 and (
                            (price - last_purchase_price) / last_purchase_price) > threshold_to_sell:
                    amount_made = current_number_of_coins * price
                    fee = amount_made * COINBASE_FEE
                    amount_made = amount_made - fee
                    current_cash_balance = current_cash_balance + amount_made
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
                    current_cash_balance = current_cash_balance - purchase_amt

                    stats_buys = stats_buys + 1

                    assert current_cash_balance >= 0

                stats_curtick_num = stats_curtick_num + 1
                last_historical_price = price

        # note: this ignores another Coinbase fee that's required to sell off the remaining coins
        total_portfolio_value = current_number_of_coins * last_historical_price + current_cash_balance

        if print_full_stats:
            print("***** threshold_to_sell: %f" % threshold_to_sell)
            print("Ending current_cash_balance: %f" % current_cash_balance)
            print("Ending current_number_of_coins: %f" % current_number_of_coins)
            print("Ending value of current_number_of_coins: %f" % (current_number_of_coins * last_historical_price))
            print("Ending total in coin OR cash: %f" % total_portfolio_value)
            print("Ending stats_buys: %d" % stats_buys)
            print("Ending stats_sells: %d" % stats_sells)
            print("Ending stats_curtick_num: %d" % stats_curtick_num)

        if print_short_stats:
            print('%f, %f, %d, %d' % (threshold_to_sell, total_portfolio_value, stats_sells, stats_buys))

        return (total_portfolio_value, stats_sells, stats_buys, stats_curtick_num, current_number_of_coins)


def run_different_thresholds():
    best_portfolio_value = WORKING_CAPITAL
    best_threshold = 0.0

    buy_and_hold_portfolio_value = WORKING_CAPITAL
    buy_and_hold_threshold = WORKING_CAPITAL

    ct = CoinTrader()
    ct.read_file(INPUT_FILENAME, 3000)

    # try different thesholds
    for i in range(5, 501, 1):
        # print(i, end=' ', flush=True)
        # print(i, flush=True)
        threshold = i / 100.0
        (total_portfolio_value, stats_sells, stats_buys, stats_curtick_num, cur_num_of_coins) = ct.run(threshold, True)

        if total_portfolio_value > best_portfolio_value:
            best_portfolio_value = total_portfolio_value
            best_threshold = threshold

        if stats_sells is 0 and stats_buys is 1:
            buy_and_hold_portfolio_value = total_portfolio_value
            buy_and_hold_threshold = threshold
            break  # no point to continue - if threshold grows even larger, no opportunity to sell

    print('****** best_portfolio_value: %f' % best_portfolio_value)
    print('best_threshold: %f' % best_threshold)
    print('buy_and_hold_portfolio_value: %f' % buy_and_hold_portfolio_value)
    print('buy_and_hold_threshold: %f' % buy_and_hold_threshold)


def run_one_threshold(threshold):
    coin_trader = CoinTrader()
    coin_trader.read_file(INPUT_FILENAME, 3000)
    coin_trader.run(threshold, True, True)


if __name__ == '__main__':
    run_different_thresholds()
    # run_one_threshold(0.05)
