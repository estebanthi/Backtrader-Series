import yfinance as yf
import backtrader as bt
import backtrader.feeds as btfeeds

from strategies import MultiTimeframeStrategy


cerebro = bt.Cerebro()

cerebro.addstrategy(MultiTimeframeStrategy)
cerebro.broker.setcash(100_000)
cerebro.broker.setcommission(commission=0.001)
cerebro.broker.set_slippage_perc(0.001)
cerebro.addsizer(bt.sizers.FixedSize, stake=1)
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade')

btc_eur = yf.Ticker("BTC-EUR")
btc_data = btc_eur.history(period="1y")
btc_pandas_data = btfeeds.PandasData(dataname=btc_data)

eth_eur = yf.Ticker("ETH-EUR")
eth_data = eth_eur.history(period="1y")
eth_pandas_data = btfeeds.PandasData(dataname=eth_data)

cerebro.adddata(btc_pandas_data)
cerebro.adddata(eth_pandas_data)
cerebro.resampledata(btc_pandas_data, timeframe=bt.TimeFrame.Weeks, compression=1)

result = cerebro.run()
