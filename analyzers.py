import backtrader as bt


class CustomAnalyzer(bt.Analyzer):
    def __init__(self):
        self._total = 0
        self._count = 0

    def notify_trade(self, trade):
        if trade.isclosed:
            self._total += trade.pnlcomm
            self._count += 1

    def get_analysis(self):
        return dict(
            average=self._total / self._count,
            total=self._total,
            count=self._count
        )
