import backtrader as bt

from backtester import Backtester
from strategies import PlotStrategy, CustomIndicatorStrat
from observers import OrderObserver, TradeObserver, BrokerObserver

observers = []

backtester = Backtester()
result, cerebro = backtester.backtest_strategy_non_optimized(CustomIndicatorStrat, stdstats=False, observers=observers)

cerebro.plot(style='candlestick', volume=False, grid=False, barup='green', bardown='red')