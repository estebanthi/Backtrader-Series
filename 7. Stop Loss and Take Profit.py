from backtester import Backtester
from strategies import BracketStrategy


backtester = Backtester()
result = backtester.backtest_strategy_non_optimized(BracketStrategy, take_profit=5)

pnl_net_total = result[0].analyzers.trade.get_analysis().pnl.net.total
print("Total PnL: {}".format(pnl_net_total))
