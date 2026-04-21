"""KuCoin kline (bar) data container."""

from __future__ import annotations

import json
import time

from bt_api_base.containers.bars.bar import BarData
from bt_api_base.functions.utils import from_dict_get_string


class KuCoinBarData(BarData):
    def __init__(self, bar_info, symbol_name, asset_type, has_been_json_encoded=False):
        super().__init__(bar_info, has_been_json_encoded)
        self.exchange_name = "KUCOIN"
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.bar_data = bar_info if has_been_json_encoded else None
        self.bar_symbol_name = None
        self.server_time = None
        self.local_update_time = time.time()
        self.period = None
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.volume = None
        self.turnover = None
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
                "bar_symbol_name": self.bar_symbol_name,
                "server_time": self.server_time,
                "period": self.period,
                "open": self.open,
                "high": self.high,
                "low": self.low,
                "close": self.close,
                "volume": self.volume,
                "turnover": self.turnover,
            }
        return self.all_data

    def __str__(self):
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self):
        return self.__str__()

    def get_exchange_name(self):
        return self.exchange_name

    def get_symbol_name(self):
        return self.symbol_name

    def get_asset_type(self):
        return self.asset_type

    def get_bar_symbol_name(self):
        return self.bar_symbol_name

    def get_server_time(self):
        return self.server_time

    def get_period(self):
        return self.period

    def get_open(self):
        return self.open

    def get_high(self):
        return self.high

    def get_low(self):
        return self.low

    def get_close(self):
        return self.close

    def get_volume(self):
        return self.volume

    def get_turnover(self):
        return self.turnover

    def get_local_update_time(self):
        return self.local_update_time

    def get_open_price(self):
        return self.open

    def get_high_price(self):
        return self.high

    def get_low_price(self):
        return self.low

    def get_close_price(self):
        return self.close


class KuCoinRequestBarData(KuCoinBarData):
    def init_data(self):
        if not self.has_been_json_encoded:
            if isinstance(self.bar_info, str):
                self.bar_data = json.loads(self.bar_info)
            else:
                self.bar_data = self.bar_info
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.bar_data, list):
            self.server_time = float(self.bar_data[0]) * 1000
            self.open = float(self.bar_data[1])
            self.close = float(self.bar_data[2])
            self.high = float(self.bar_data[3])
            self.low = float(self.bar_data[4])
            self.volume = float(self.bar_data[5])
            self.turnover = float(self.bar_data[6]) if len(self.bar_data) > 6 else 0.0
        elif isinstance(self.bar_data, dict) and "data" in self.bar_data:
            data = self.bar_data["data"]
            if isinstance(data, list) and len(data) > 0:
                kline = data[0]
                self.server_time = float(kline[0]) * 1000
                self.open = float(kline[1])
                self.close = float(kline[2])
                self.high = float(kline[3])
                self.low = float(kline[4])
                self.volume = float(kline[5])
                self.turnover = float(kline[6]) if len(kline) > 6 else 0.0

        self.bar_symbol_name = self.symbol_name
        self.period = None
        self.has_been_init_data = True
        return self


class KuCoinWssBarData(KuCoinBarData):
    def init_data(self):
        if not self.has_been_json_encoded:
            self.bar_data = json.loads(self.bar_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.bar_data, dict) and "data" in self.bar_data:
            data = self.bar_data["data"]
            candles = data.get("candles", [])
            if candles:
                self.server_time = float(candles[0]) * 1000
                self.open = float(candles[1])
                self.close = float(candles[2])
                self.high = float(candles[3])
                self.low = float(candles[4])
                self.volume = float(candles[5])
                self.turnover = float(candles[6]) if len(candles) > 6 else 0.0
            self.bar_symbol_name = from_dict_get_string(data, "symbol")

        self.period = None
        self.has_been_init_data = True
        return self
