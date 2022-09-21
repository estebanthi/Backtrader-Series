from backtester import Backtester
from strategies import CustomIndicatorStrat


backtester = Backtester()
result = backtester.backtest_strategy_non_optimized(CustomIndicatorStrat, doji_threshold=5)

pnl_net_total = result[0].analyzers.trade.get_analysis().pnl.net.total
print("Total PnL: {}".format(pnl_net_total))
