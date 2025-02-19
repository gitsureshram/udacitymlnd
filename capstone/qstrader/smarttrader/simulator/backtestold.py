from __future__ import print_function

from common.compat import queue
from common.compat import queue
from environment.event import EventType
from common.PropertyReader import *
from dateutil import parser
import json
import smarttrader.indicators.TopoSort as topoSort

class Backtest(object):
    """
    Enscapsulates the settings and components for
    carrying out an event-driven backtest.
    """

    def __init__(self, agent, price_handler=None,
                 strategy=None, portfolio_handler=None,
                 execution_handler=None,
                 position_sizer=None, risk_manager=None,
                 statistics=None, equity=None):

        if agent != None:

            self.agent = agent
            self.price_handler = agent.price_handler
            self.strategy = agent.strategy
            self.portfolio_handler = agent.portfolio_handler
            self.execution_handler = agent.execution_handler
            self.position_sizer = agent.position_sizer
            self.risk_manager = agent.risk_manager
            self.statistics = agent.statistics
            self.equity = agent.initial_equity
            self.events_queue = agent.price_handler.events_queue
            self.cur_time = None
            self.indicator_list = agent.indicator_list
            self.indicator_dict = agent.indicator_dict

        else:

            self.price_handler = price_handler
            self.strategy = strategy
            self.portfolio_handler = portfolio_handler
            self.execution_handler = execution_handler
            self.position_sizer = position_sizer
            self.risk_manager = risk_manager
            self.statistics = statistics
            self.equity = equity
            self.events_queue = price_handler.events_queue
            self.cur_time = None

    def _run_backtest(self):
        """
        Carries out an infinite while loop that polls the
        events queue and directs each event to either the
        strategy component of the execution handler. The
        loop continue until the event queue has been
        emptied.
        """
        print("Running Backtest...")
        while self.price_handler.continue_backtest:
            try:
                event = self.events_queue.get(False)
            except queue.Empty:
                self.price_handler.stream_next()
            else:
                if event is not None:
                    if event.type == EventType.TICK or event.type == EventType.BAR:
                        self.cur_time = event.time
                        self.strategy.calculate_signals(event,self.agent)
                        self.portfolio_handler.update_portfolio_value()
                        self.statistics.update(event.time, self.portfolio_handler)
                    elif event.type == EventType.SIGNAL:
                        self.portfolio_handler.on_signal(event)
                    elif event.type == EventType.ORDER:
                        self.execution_handler.execute_order(event)
                    elif event.type == EventType.FILL:
                        self.portfolio_handler.on_fill(event)
                    else:
                        raise NotImplemented("Unsupported event.type '%s'" % event.type)

    def simulate_trading(self, filename=None,testing=False):
        """
        Simulates the backtest and outputs portfolio performance.
        """
        self._run_backtest()
        results = self.statistics.get_results()

        print (results)
        print("---------------------------------")
        print("Backtest complete.")
        print("Sharpe Ratio: %s" % results["sharpe"])
        print("Max Drawdown: %s" % results["max_drawdown"])
        print("Max Drawdown Pct: %s" % results["max_drawdown_pct"])
        if not testing:
            self.statistics.plot_results()
        return ""
