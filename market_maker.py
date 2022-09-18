from enum import Enum


class Dir(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class MarketMaker():
    def __init__(self, exchange):
        self._exchange = exchange
        self._BASE_OID = 4_000_000
        self._delta = 1
        self._assets = ['BOND', 'GS', 'MS', 'VALBZ', 'VALE', 'WFC', 'XLF']

        # one unique order id for each asset and side, e.g. 'WFC' and 'B'
        self._oid = {}
        for asset in self._assets:
            self._oid[asset+'B'] = self._BASE_OID + 1
            self._oid[asset+'S'] = self._BASE_OID + 2
            self._BASE_OID += 2

    def listen(self, msg):
        '''
        If a newly confirmed trade is broadcasted, cancel all pending
        orders for said asset and place two new ones, a buy order at
        txn_price-1 and a sell order at txn_price+1.
        '''

        if msg['type'] != 'trade':
            return

        if msg['symbol'] not in self._assets:
            return

        sym = msg['symbol']
        prc = msg['price']

        b_prc = prc - self._delta
        s_prc = prc + self._delta

        b_oid = self._oid[sym+'B']
        s_oid = self._oid[sym+'S']

        # cancel existing orders
        self._exchange.send_cancel_message(order_id=b_oid)
        self._exchange.send_cancel_message(order_id=s_oid)

        # add new orders
        self._exchange.send_add_message(order_id=b_oid, symbol=sym, dir=Dir.BUY , price=b_prc, size=1)
        self._exchange.send_add_message(order_id=s_oid, symbol=sym, dir=Dir.SELL, price=s_prc, size=1)