"""KuCoin trade data container."""

from __future__ import annotations

import json
import time

from bt_api_base.containers.trades.trade import TradeData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class KuCoinTradeData(TradeData):
    def __init__(self, trade_info, symbol_name, asset_type, has_been_json_encoded=False):
        super().__init__(trade_info, has_been_json_encoded)
        self.exchange_name = "KUCOIN"
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.trade_data = trade_info if has_been_json_encoded else None
        self.trade_symbol_name = None
        self.server_time = None
        self.trade_id = None
        self.trade_price = None
        self.trade_size = None
        self.trade_side = None
        self.all_data = None
        self.has_been_init_data = False

    def init_data(self):
        raise NotImplementedError("Subclasses must implement init_data")

    def get_all_data(self):
        if self.all_data is None:
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "trade_symbol_name": self.trade_symbol_name,
                "server_time": self.server_time,
                "trade_id": self.trade_id,
                "trade_price": self.trade_price,
                "trade_size": self.trade_size,
                "trade_side": self.trade_side,
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
        return time.time()

    def get_symbol_name(self):
        return self.symbol_name

    def get_asset_type(self):
        return self.asset_type

    def get_trade_symbol_name(self):
        return self.trade_symbol_name

    def get_server_time(self):
        return self.server_time

    def get_trade_id(self):
        return self.trade_id

    def get_trade_price(self):
        return self.trade_price

    def get_trade_size(self):
        return self.trade_size

    def get_trade_side(self):
        return self.trade_side


class KuCoinRequestTradeData(KuCoinTradeData):
    def init_data(self):
        if not self.has_been_json_encoded:
            self.trade_data = json.loads(self.trade_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.trade_data, dict) and "data" in self.trade_data:
            data = self.trade_data["data"]
            if isinstance(data, list) and len(data) > 0:
                data = data[0]
        else:
            data = self.trade_data

        self.trade_symbol_name = self.symbol_name
        self.server_time = from_dict_get_float(data, "time")
        self.trade_id = from_dict_get_string(data, "sequence") or str(from_dict_get_float(data, "time"))
        self.trade_price = from_dict_get_float(data, "price")
        self.trade_size = from_dict_get_float(data, "size")
        self.trade_side = from_dict_get_string(data, "side")

        self.has_been_init_data = True
        return self


class KuCoinWssTradeData(KuCoinTradeData):
    def init_data(self):
        if not self.has_been_json_encoded:
            self.trade_data = json.loads(self.trade_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.trade_data, dict) and "data" in self.trade_data:
            data = self.trade_data["data"]
        else:
            data = self.trade_data

        self.trade_symbol_name = self.symbol_name
        self.server_time = from_dict_get_float(data, "time")
        self.trade_id = from_dict_get_string(data, "tradeId") or from_dict_get_string(data, "sequence")
        self.trade_price = from_dict_get_float(data, "price")
        self.trade_size = from_dict_get_float(data, "size")
        self.trade_side = from_dict_get_string(data, "side")

        self.has_been_init_data = True
        return self


class KuCoinFillTradeData(KuCoinTradeData):
    def init_data(self):
        if not self.has_been_json_encoded:
            self.trade_data = json.loads(self.trade_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.trade_data, dict) and "data" in self.trade_data:
            data = self.trade_data["data"]
            if "items" in data and isinstance(data["items"], list) and len(data["items"]) > 0:
                data = data["items"][0]
            elif isinstance(data, list) and len(data) > 0:
                data = data[0]
        else:
            data = self.trade_data

        self.trade_symbol_name = from_dict_get_string(data, "symbol")
        self.server_time = from_dict_get_float(data, "createdAt")
        self.trade_id = from_dict_get_string(data, "tradeId")
        self.trade_price = from_dict_get_float(data, "price")
        self.trade_size = from_dict_get_float(data, "size")
        self.trade_side = from_dict_get_string(data, "side")

        self.has_been_init_data = True
        return self
