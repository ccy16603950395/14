class QMTAdapter:
    """研究环境占位接口，不连接实盘。"""
    def get_positions(self): raise NotImplementedError
    def get_cash(self): raise NotImplementedError
    def get_market_data(self, symbols, start_date=None, end_date=None): raise NotImplementedError
    def submit_order(self, symbol, side, qty, order_type='market', price=None): raise NotImplementedError
    def cancel_order(self, order_id): raise NotImplementedError
    def rebalance_to_target_weights(self, target_weights): raise NotImplementedError
