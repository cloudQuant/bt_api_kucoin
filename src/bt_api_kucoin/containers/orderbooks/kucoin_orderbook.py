"""KuCoin orderbook data container."""

from __future__ import annotations

import json
import time

from bt_api_base.containers.orderbooks.orderbook import OrderBookData
from bt_api_base.functions.utils import from_dict_get_float


class KuCoinOrderBookData(OrderBookData):
    def __init__(self, order_book_info, symbol_name, asset_type, has_been_json_encoded=False):
        super().__init__(order_book_info, has_been_json_encoded)
        self.exchange_name = "KUCOIN"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.order_book_data = order_book_info if has_been_json_encoded else None
        self.order_book_symbol_name = None
        self.server_time = None
        self.bid_price_list = None
        self.ask_price_list = None
        self.bid_volume_list = None
        self.ask_volume_list = None
        self.bid_trade_nums = None
        self.ask_trade_nums = None
        self.all_data = None
        self.has_been_init_data = False

    def init_data(self):
        raise NotImplementedError("Subclasses must implement init_data")

    def get_all_data(self):
        if self.all_data is None:
            self.all_data = {
                "exchange_name": self.exchange_name,
                "asset_type": self.asset_type,
                "symbol_name": self.symbol_name,
                "order_book_symbol_name": self.order_book_symbol_name,
                "local_update_time": self.local_update_time,
                "server_time": self.server_time,
                "bid_price_list": self.bid_price_list,
                "ask_price_list": self.ask_price_list,
                "bid_volume_list": self.bid_volume_list,
                "ask_volume_list": self.ask_volume_list,
                "bid_trade_nums": self.bid_trade_nums,
                "ask_trade_nums": self.ask_trade_nums,
            }
        return self.all_data

    def __str__(self):
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self):
        return self.__str__()

    def get_exchange_name(self):
        return self.exchange_name

    def get_local_update_time(self):
        return self.local_update_time

    def get_symbol_name(self):
        return self.symbol_name

    def get_asset_type(self):
        return self.asset_type

    def get_server_time(self):
        return self.server_time

    def get_bid_price_list(self):
        return self.bid_price_list

    def get_ask_price_list(self):
        return self.ask_price_list

    def get_bid_volume_list(self):
        return self.bid_volume_list

    def get_ask_volume_list(self):
        return self.ask_volume_list

    def get_bid_trade_nums(self):
        return self.bid_trade_nums

    def get_ask_trade_nums(self):
        return self.ask_trade_nums


class KuCoinRequestOrderBookData(KuCoinOrderBookData):
    def init_data(self):
        if not self.has_been_json_encoded:
            self.order_book_info = json.loads(self.order_book_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        self.order_book_data = self.order_book_info.get("data", {})
        self.order_book_symbol_name = self.symbol_name
        self.server_time = from_dict_get_float(self.order_book_data, "time")

        bids = self.order_book_data.get("bids", [])
        asks = self.order_book_data.get("asks", [])

        self.bid_price_list = [float(level[0]) for level in bids]
        self.bid_volume_list = [float(level[1]) for level in bids]
        self.bid_trade_nums = [float(level[2]) if len(level) > 2 else 1.0 for level in bids]

        self.ask_price_list = [float(level[0]) for level in asks]
        self.ask_volume_list = [float(level[1]) for level in asks]
        self.ask_trade_nums = [float(level[2]) if len(level) > 2 else 1.0 for level in asks]

        self.has_been_init_data = True
        return self


class KuCoinWssOrderBookData(KuCoinOrderBookData):
    def init_data(self):
        if not self.has_been_json_encoded:
            self.order_book_info = json.loads(self.order_book_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        data = self.order_book_info.get("data", {})
        self.order_book_data = data
        self.order_book_symbol_name = self.symbol_name
        self.server_time = time.time() * 1000

        bids = data.get("bids", [])
        asks = data.get("asks", [])

        self.bid_price_list = [float(level[0]) for level in bids]
        self.bid_volume_list = [float(level[1]) for level in bids]
        self.bid_trade_nums = [float(level[2]) if len(level) > 2 else 1.0 for level in bids]

        self.ask_price_list = [float(level[0]) for level in asks]
        self.ask_volume_list = [float(level[1]) for level in asks]
        self.ask_trade_nums = [float(level[2]) if len(level) > 2 else 1.0 for level in asks]

        self.has_been_init_data = True
        return self


class KuCoinLevel3OrderBookData(KuCoinOrderBookData):
    def init_data(self):
        if not self.has_been_json_encoded:
            self.order_book_info = json.loads(self.order_book_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        self.order_book_data = self.order_book_info.get("data", {})
        self.order_book_symbol_name = self.symbol_name
        self.server_time = from_dict_get_float(self.order_book_data, "sequence")

        bids = self.order_book_data.get("bids", [])
        asks = self.order_book_data.get("asks", [])

        bid_dict: dict[float | str, float] = {}
        ask_dict: dict[float | str, float] = {}

        for _order_id, price, size in bids:
            price_float = float(price)
            size_float = float(size)
            orders_key = f"{price_float}_orders"
            if price_float in bid_dict:
                bid_dict[price_float] += size_float
                bid_dict[orders_key] = bid_dict.get(orders_key, 0) + 1
            else:
                bid_dict[price_float] = size_float
                bid_dict[orders_key] = 1

        for _order_id, price, size in asks:
            price_float = float(price)
            size_float = float(size)
            orders_key = f"{price_float}_orders"
            if price_float in ask_dict:
                ask_dict[price_float] += size_float
                ask_dict[orders_key] = ask_dict.get(orders_key, 0) + 1
            else:
                ask_dict[price_float] = size_float
                ask_dict[orders_key] = 1

        self.bid_price_list = sorted([k for k in bid_dict if isinstance(k, float)], reverse=True)
        self.bid_volume_list = [bid_dict[p] for p in self.bid_price_list]
        self.bid_trade_nums = [int(bid_dict.get(f"{p}_orders", 1)) for p in self.bid_price_list]

        self.ask_price_list = sorted([k for k in ask_dict if isinstance(k, float)])
        self.ask_volume_list = [ask_dict[p] for p in self.ask_price_list]
        self.ask_trade_nums = [int(ask_dict.get(f"{p}_orders", 1)) for p in self.ask_price_list]

        self.has_been_init_data = True
        return self
