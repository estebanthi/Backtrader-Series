import backtrader as bt


class Doji(bt.Indicator):
    lines = ('is_doji',)
    params = (
        ('threshold_percent', 5),
    )

    def next(self):
        open = self.data.open[0]
        close = self.data.close[0]
        high = self.data.high[0]
        low = self.data.low[0]
        threshold = (high - low) * self.p.threshold_percent / 100
        self.lines.is_doji[0] = abs(open - close) < threshold and high - low > threshold
