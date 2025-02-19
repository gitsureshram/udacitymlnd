from smarttrader.position.position import Position


class Portfolio(object):
    def __init__(self, price_handler, cash):

        self.price_handler = price_handler
        self.init_cash = cash
        self.equity = cash
        self.cur_cash = cash
        self.positions = {}
        self.closed_positions = []
        self.realised_pnl = 0

        from collections import deque
        self.value_queue = deque(maxlen=100 )

    def _update_portfolio(self):

        self.unrealised_pnl = 0
        self.equity = self.realised_pnl
        self.equity += self.init_cash

        for ticker in self.positions:
            pt = self.positions[ticker]
            if self.price_handler.istick():
                bid, ask = self.price_handler.get_best_bid_ask(ticker)
            else:
                close_price = self.price_handler.get_last_close(ticker)
                bid = close_price
                ask = close_price
            pt.update_market_value(bid, ask)
            self.unrealised_pnl += pt.unrealised_pnl
            pnl_diff = pt.realised_pnl - pt.unrealised_pnl
            self.equity += (
                pt.market_value - pt.cost_basis + pnl_diff
            )
            self.value_queue.append(self.equity )

    def _add_position(
        self, action, ticker,
        quantity, price, commission
    ):

        if ticker not in self.positions:
            if self.price_handler.istick():
                bid, ask = self.price_handler.get_best_bid_ask(ticker)
            else:
                close_price = self.price_handler.get_last_close(ticker)
                bid = close_price
                ask = close_price
            position = Position(
                action, ticker, quantity,
                price, commission, bid, ask
            )
            self.positions[ticker] = position
            self._update_portfolio()
        else:
            print(
                "Ticker %s is already in the positions list. "
                "Could not add a new position." % ticker
            )

    def _modify_position(
        self, action, ticker,
        quantity, price, commission
    ):

        if ticker in self.positions:
            self.positions[ticker].transact_shares(
                action, quantity, price, commission
            )
            if self.price_handler.istick():
                bid, ask = self.price_handler.get_best_bid_ask(ticker)
            else:
                close_price = self.price_handler.get_last_close(ticker)
                bid = close_price
                ask = close_price
            self.positions[ticker].update_market_value(bid, ask)

            if self.positions[ticker].quantity == 0:
                closed = self.positions.pop(ticker)
                self.realised_pnl += closed.realised_pnl
                self.closed_positions.append(closed)

            self._update_portfolio()
        else:
            print(
                "Ticker %s not in the current position list. "
                "Could not modify a current position." % ticker
            )

    def transact_position(
        self, action, ticker,
        quantity, price, commission
    ):


        if action == "BOT":
            self.cur_cash -= ((quantity * price) + commission)
        elif action == "SLD":
            self.cur_cash += ((quantity * price) - commission)

        if ticker not in self.positions:
            self._add_position(
                action, ticker, quantity,
                price, commission
            )
        else:
            self._modify_position(
                action, ticker, quantity,
                price, commission
            )
