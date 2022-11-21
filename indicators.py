import backtrader as bt


class Doji(bt.Indicator):
    lines = ('is_doji', 'doji_price')
    params = (
        ('threshold_percent', 5),
    )

    plotinfo = dict(
        plot=False,
    )

    def next(self):
        open = self.data.open[0]
        close = self.data.close[0]
        high = self.data.high[0]
        low = self.data.low[0]
        threshold = (high - low) * self.p.threshold_percent / 100
        self.lines.is_doji[0] = abs(open - close) < threshold and high - low > threshold
        self.lines.doji_price[0] = (open + close) / 2 if self.lines.is_doji[0] else 0

class DelayedPrice(bt.Indicator):
    lines = ('delayed_price',)
    params = (
        ('delay', 1),
    )

    plotinfo = dict(subplot=False)

    plotlines = dict(
        delayed_price=dict(
            _name='Delayed Price',
            color='blue',
            linestyle='--',
            linewidth=1,
        ),
    )

    def next(self):
        self.lines.delayed_price[0] = self.data.close[-self.p.delay]