import backtrader as bt


class BrokerObserver(bt.Observer):
    lines = ('cash', 'value', 'commission', 'pnl')

    plotinfo = dict(plot=True, subplot=True, plotlinelabels=True)

    plotlines = dict(
        cash=dict(
            _name='Cash',
            color='blue',
            linewidth=1,
        ),
        value=dict(
            _name='Value',
            color='green',
            linewidth=1,
        ),
        pnl=dict(
            _name='PnL',
            color='black',
            linewidth=1,
        ),
    )

    def next(self):
        self.lines.cash[0] = self._owner.broker.get_cash()
        self.lines.value[0] = self._owner.broker.get_value()
        self.lines.pnl[0] = self._owner.broker.get_value() - self._owner.broker.startingcash

    def next(self):
        self.lines.cash[0] = self._owner.broker.get_cash()
        self.lines.value[0] = self._owner.broker.get_value()
        self.lines.pnl[0] = self._owner.broker.get_value() - self._owner.broker.get_cash()


class OrderObserver(bt.observer.Observer):
    lines = ('created', 'expired',)

    plotinfo = dict(plot=True, subplot=True, plotlinelabels=True)

    plotlines = dict(
        created=dict(marker='*', markersize=8.0, color='lime', fillstyle='full'),
        expired=dict(marker='s', markersize=8.0, color='red', fillstyle='full')
    )

    def next(self):
        for order in self._owner._orderspending:
            if order.data is not self.data:
                continue

            if order.status in [bt.Order.Accepted, bt.Order.Submitted]:
                self.lines.created[0] = order.created.price

            elif order.status in [bt.Order.Expired]:
                self.lines.expired[0] = order.created.price


class TradeObserver(bt.observer.Observer):
    lines = ('entry', 'exit',)

    plotinfo = dict(plot=True, subplot=True, plotlinelabels=True)

    plotlines = dict(
        entry=dict(marker='^', markersize=8.0, color='blue', fillstyle='full'),
        exit=dict(marker='v', markersize=8.0, color='orange', fillstyle='full')
    )

    def next(self):
        for trade in self._owner._tradespending:
            if trade.data is not self.data:
                continue

            if trade.status in [bt.Trade.Open]:
                self.lines.entry[0] = trade.price

            elif trade.status in [bt.Trade.Closed]:
                self.lines.exit[0] = trade.price