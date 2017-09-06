import unittest

from coin_trader import CoinTrader


class TestCoinTrader(unittest.TestCase):
    def test_date_ranges(self):
        data1 = [
            "1417411980,300,300,300,300,0.01,3,300",  # 12/01/2014 @ 5:33am (UTC)
            "1462913100,455.53,455.85,455.45,455.85,2.50018,1139.5138893,455.77274009",  # 05/10/2016 @ 8:45pm (UTC)
            "1496188800,2191.6,2192.53,2188.8,2188.8,24.67996163,54086.74637,2191.524735"  # 05/31/2017 @ 12:00am (UTC)
        ]
        coin_trader1 = CoinTrader()
        coin_trader1.read_data(data1, 300)
        self.assertEqual(len(coin_trader1.dataset), 3, 'overall dataset')
        coin_trader1.read_data(data1, 1)
        (total_portfolio_value, stats_sells, stats_buys, stats_curtick_num, cur_num_of_coins) = coin_trader1.run(1)
        self.assertEqual(stats_curtick_num, 1)
        coin_trader1.read_data(data1, 400)
        (total_portfolio_value, stats_sells, stats_buys, stats_curtick_num, cur_num_of_coins) = coin_trader1.run(1)
        self.assertEqual(stats_curtick_num, 2)

    def test_number_of_trades(self):
        data1 = [
            "1417411980,300,300,300,300,0.01,3,300",  # 12/01/2014 @ 5:33am (UTC)
            "1462913100,455.53,455.85,455.45,455.85,2.50018,1139.5138893,455.77274009",  # 05/10/2016 @ 8:45pm (UTC)
            "1496188800,2191.6,2192.53,2188.8,2188.8,24.67996163,54086.74637,2191.524735"  # 05/31/2017 @ 12:00am (UTC)
        ]
        coin_trader1 = CoinTrader()
        coin_trader1.read_data(data1, 3000)
        (total_portfolio_value, stats_sells, stats_buys, stats_curtick_num,
         cur_num_of_coins) = coin_trader1.run(0.01)
        self.assertEqual(stats_curtick_num, 3)
        self.assertEqual(stats_sells, 2)
        self.assertEqual(stats_buys, 3)

    def test_buy_and_hold(self):
        data1 = [
            "1417411980,300,300,300,300,0.01,3,300",  # 12/01/2014 @ 5:33am (UTC)
            "1462913100,455.53,455.85,455.45,455.85,2.50018,1139.5138893,455.77274009",  # 05/10/2016 @ 8:45pm (UTC)
            "1496188800,2191.6,2192.53,2188.8,2188.8,24.67996163,54086.74637,2191.524735"  # 05/31/2017 @ 12:00am (UTC)
        ]
        coin_trader1 = CoinTrader()
        coin_trader1.read_data(data1, 3000)
        # run it with a high threshold
        (total_portfolio_value, stats_sells, stats_buys, stats_curtick_num, cur_num_of_coins) = coin_trader1.run(1000)
        self.assertEqual(total_portfolio_value, 71599.572)
        self.assertEqual(stats_sells, 0)
        self.assertEqual(stats_buys, 1)
        self.assertEqual(stats_curtick_num, 3)
        self.assertEqual(cur_num_of_coins, 32.67)

    def test_sell_every_tick1(self):
        data1 = [
            "1417411980,300,300,300,300,0.01,3,300",  # 12/01/2014 @ 5:33am (UTC)
            "1462913100,455.53,455.85,455.45,455.85,2.50018,1139.5138893,455.77274009",  # 05/10/2016 @ 8:45pm (UTC)
            "1496188800,2191.6,2192.53,2188.8,2188.8,24.67996163,54086.74637,2191.524735"  # 05/31/2017 @ 12:00am (UTC)
        ]
        coin_trader1 = CoinTrader()
        coin_trader1.read_data(data1, 3000)
        # run it with a low threshold
        (total_portfolio_value, stats_sells, stats_buys, stats_curtick_num, cur_num_of_coins) = coin_trader1.run(0.001)
        self.assertEqual(total_portfolio_value, 50602.2365751317)
        self.assertEqual(stats_sells, 2)
        self.assertEqual(stats_buys, 3)
        self.assertEqual(stats_curtick_num, 3)
        self.assertEqual(cur_num_of_coins, 4.472075196203687)

    def test_sell_every_tick2(self):
        data1 = [
            "1417411980,300,300,300,300,0.01,3,300",  # 12/01/2014 @ 5:33am (UTC)
            "1462913100,455.53,455.85,455.45,455.85,2.50018,1139.5138893,455.77274009",  # 05/10/2016 @ 8:45pm (UTC)
            "1496188800,2191.6,2192.53,2188.8,2188.8,24.67996163,54086.74637,2191.524735"  # 05/31/2017 @ 12:00am (UTC)
        ]
        coin_trader1 = CoinTrader()
        coin_trader1.read_data(data1, 3000)
        # run it with a low threshold
        (total_portfolio_value, stats_sells, stats_buys, stats_curtick_num, cur_num_of_coins) = coin_trader1.run(0.5)
        self.assertEqual(total_portfolio_value, 50602.2365751317)
        self.assertEqual(stats_sells, 2)
        self.assertEqual(stats_buys, 3)
        self.assertEqual(stats_curtick_num, 3)
        self.assertEqual(cur_num_of_coins, 4.472075196203687)

    def test_sell_once(self):
        data1 = [
            "1417411980,300,300,300,300,0.01,3,300",  # 12/01/2014 @ 5:33am (UTC)
            "1462913100,455.53,455.85,455.45,455.85,2.50018,1139.5138893,455.77274009",  # 05/10/2016 @ 8:45pm (UTC)
            "1496188800,2191.6,2192.53,2188.8,2188.8,24.67996163,54086.74637,2191.524735"  # 05/31/2017 @ 12:00am (UTC)
        ]
        coin_trader1 = CoinTrader()
        coin_trader1.read_data(data1, 3000)
        # first price spike is 0.518433333, let's exclude it with a threshold slightly larger than that
        (total_portfolio_value, stats_sells, stats_buys, stats_curtick_num, cur_num_of_coins) = coin_trader1.run(0.52)
        self.assertEqual(total_portfolio_value, 69975.7405172)
        self.assertEqual(stats_sells, 1)
        self.assertEqual(stats_buys, 2)
        self.assertEqual(stats_curtick_num, 3)
        self.assertEqual(cur_num_of_coins, 4.472075196203687)

if __name__ == '__main__':
    unittest.main()
