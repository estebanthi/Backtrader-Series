import backtrader as bt
from termcolor import colored

from backtrader.indicators import ExponentialMovingAverage as EMA
from indicators import Doji


class MyStrategy(bt.Strategy):
    params = (
        ('ema_period', 10),
    )

    def __init__(self):
       self.ema = EMA(period=self.p.ema_period)

    def log(self, msg, dt=None):
        print("{} - {}".format(dt or self.datas[0].datetime.date(0), msg))

    def next(self):
        self.log('Close: {}, EMA: {}'.format(self.datas[0].close[0], self.ema[0]))

        if not self.position:

            if self.datas[0].close[0] < self.ema[0]:
                self.log('BUY CREATE, %.2f' % self.datas[0].close[0])
                orders = [self.buy()]
                self.orders_ref = [order.ref for order in orders if order]

        if self.datas[0].close[0] > self.ema[0]:
            self.close()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

            # Check if an order has been completed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(colored('BUY EXECUTED, %.2f' % order.executed.price, 'blue'))
                self.buy_price = order.executed.price
            elif order.issell():
                self.log(colored('SELL EXECUTED, %.2f' % order.executed.price, 'yellow'))

            # Not enough cash: order rejected
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

            # We remove order if it's useless
        if not order.alive() and order.ref in self.orders_ref:
            self.orders_ref.remove(order.ref)

    def notify_trade(self, trade):
        if trade.isclosed:
            self.log(colored('PROFIT, %.2f' % (trade.pnl), 'green') if trade.pnl > 0
                     else colored('LOSS, %.2f' % (trade.pnl), 'red'))


class CustomIndicatorStrat(bt.Strategy):

    params = (
        ('doji_threshold', 5),
    )

    def __init__(self):
        self.doji = Doji(threshold_percent=self.p.doji_threshold)
        self.candle_open = 0

    def log(self, msg, dt=None):
        print("{} - {}".format(dt or self.datas[0].datetime.date(0), msg))

    def next(self):
        self.log('Close: {}, IsDoji: {}'.format(self.datas[0].close[0], self.doji.is_doji[0]))

        if not self.position:
            if self.doji.is_doji[0]:
                self.log('BUY CREATE, %.2f' % self.datas[0].close[0])
                orders = [self.buy()]
                self.orders_ref = [order.ref for order in orders if order]
                self.candle_open = len(self)

        if len(self) > (self.candle_open + 3):
            self.close()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

            # Check if an order has been completed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(colored('BUY EXECUTED, %.2f' % order.executed.price, 'blue'))
                self.buy_price = order.executed.price
            elif order.issell():
                self.log(colored('SELL EXECUTED, %.2f' % order.executed.price, 'yellow'))

            # Not enough cash: order rejected
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

            # We remove order if it's useless
        if not order.alive() and order.ref in self.orders_ref:
            self.orders_ref.remove(order.ref)

    def notify_trade(self, trade):
        if trade.isclosed:
            self.log(colored('PROFIT, %.2f' % (trade.pnl), 'green') if trade.pnl > 0
                     else colored('LOSS, %.2f' % (trade.pnl), 'red'))
