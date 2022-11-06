from backtester import Backtester
from strategies import BracketStrategy

from analyzers import CustomAnalyzer


if __name__ == '__main__':
    result = Backtester.backtest_strategy_non_optimized(
        BracketStrategy,
        analyzers=[CustomAnalyzer],
        stop_loss=1,
        take_profit=2
    )
    print(result[0].analyzers.customanalyzer.get_analysis())
