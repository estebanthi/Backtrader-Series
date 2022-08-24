import backtrader as bt
import backtrader.feeds as btfeeds
import yfinance as yf
from termcolor import colored

from backtrader.indicators import ExponentialMovingAverage as EMA


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


btc_eur = yf.Ticker("BTC-EUR")
data = btc_eur.history(period="1y")
pandas_data = btfeeds.PandasData(dataname=data)

cerebro = bt.Cerebro()

cerebro.adddata(pandas_data)
cerebro.addstrategy(MyStrategy, ema_period=10)
cerebro.broker.setcash(100_000)
cerebro.broker.setcommission(commission=0.001)
cerebro.broker.set_slippage_perc(0.001)
cerebro.addsizer(bt.sizers.FixedSize, stake=1)
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade')

result = cerebro.run()
strategy_result = result[0]
trade_analyzer = strategy_result.analyzers.trade
analysis = trade_analyzer.get_analysis()

pnl_net_total = analysis.pnl.net.total
pnl_gross_total = analysis.pnl.gross.total
commissions = pnl_gross_total - pnl_net_total

winners = analysis.won.total
losers = analysis.lost.total
win_rate = winners / (winners + losers) * 100

print("---ANALYSIS---")
print("PnL net total: {}".format(pnl_net_total))
print("PnL gross total: {}".format(pnl_gross_total))
print("Commissions: {}".format(commissions))
print("Win rate: {}".format(win_rate))

cerebro.plot()
