import backtrader as bt
import backtrader.feeds as btfeeds
import yfinance as yf

from strategy import MyStrategy
from utils import get_params_from_strategy_result


def backtest_strategy_non_optimized(strategy, **parameters):
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

    result = cerebro.run()
    return result


result = backtest_strategy_non_optimized(MyStrategy, ema_period=10)


def backtest_strategy_optimized(strategy, **parameters):
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

    result = cerebro.run(maxcpus=1, optreturn=False)
    return result, cerebro


result, cerebro = backtest_strategy_optimized(MyStrategy, ema_period=range(5, 10))
print(result)

for res in result:
    strat_result = res[0]
    params = get_params_from_strategy_result(strat_result)
    analysis = strat_result.analyzers.trade.get_analysis()
    total_net_pnl = analysis.pnl.net.total
    print(f"Parameters: {params} | Total Net PNL: {total_net_pnl}")


cerebro.plot()
