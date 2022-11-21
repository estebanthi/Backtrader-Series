import backtrader as bt
import backtrader.feeds as btfeeds
import yfinance as yf


class Backtester:

    @staticmethod
    def backtest_strategy_non_optimized(strategy, analyzers=None, stdstats=True, observers=None, **parameters):
        btc_eur = yf.Ticker("BTC-EUR")
        data = btc_eur.history(period="1y")
        pandas_data = btfeeds.PandasData(dataname=data)

        cerebro = bt.Cerebro()

        cerebro.adddata(pandas_data)
        cerebro.addstrategy(strategy, **parameters)
        cerebro.broker.setcash(100_000)
        cerebro.broker.setcommission(commission=0.001)
        cerebro.broker.set_slippage_perc(0.001)
        cerebro.addsizer(bt.sizers.FixedSize, stake=1)
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade')

        if not analyzers:
            analyzers = []
        for analyzer in analyzers:
            cerebro.addanalyzer(analyzer, _name=analyzer.__name__.lower())

        if not observers:
            observers = []
        for observer in observers:
            cerebro.addobserver(observer)

        result = cerebro.run(stdstats=stdstats)
        return result, cerebro

    @staticmethod
    def backtest_strategy_optimized(strategy, analyzers=None, **parameters):
        btc_eur = yf.Ticker("BTC-EUR")
        data = btc_eur.history(period="1y")
        pandas_data = btfeeds.PandasData(dataname=data)

        cerebro = bt.Cerebro()

        cerebro.adddata(pandas_data)
        cerebro.optstrategy(strategy, **parameters)
        cerebro.broker.setcash(100_000)
        cerebro.broker.setcommission(commission=0.001)
        cerebro.broker.set_slippage_perc(0.001)
        cerebro.addsizer(bt.sizers.FixedSize, stake=1)
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade')

        if not analyzers:
            analyzers = []
        for analyzer in analyzers:
            cerebro.addanalyzer(analyzer, _name=analyzer.__name__.lower())

        result = cerebro.run(maxcpus=1, optreturn=False)
        return result, cerebro
