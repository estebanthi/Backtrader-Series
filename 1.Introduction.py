import backtrader as bt
import backtrader.feeds as btfeeds
import yfinance as yf

btc_eur = yf.Ticker("BTC-EUR")
data = btc_eur.history()
pandas_data = btfeeds.PandasData(dataname=data)


class MyFirstStrat(bt.Strategy):

    def next(self):
        print(self.datas[0].close[0])


cerebro = bt.Cerebro()
cerebro.adddata(pandas_data)
cerebro.addstrategy(MyFirstStrat)

cerebro.run()
