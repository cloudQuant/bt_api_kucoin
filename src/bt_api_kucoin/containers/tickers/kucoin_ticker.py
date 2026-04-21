"""KuCoin ticker data container."""

from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base._compat import Self
from bt_api_base.containers.tickers.ticker import TickerData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class KuCoinTickerData(TickerData):
    def __init__(self, ticker_info, symbol_name, asset_type, has_been_json_encoded=False) -> None:
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = "KUCOIN"
        self.local_update_time = time.time()
        self.ticker_data: dict[str, Any] | None = ticker_info if has_been_json_encoded else None
        self.ticker_symbol_name: str | None = None
        self.has_been_init_data = False
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.server_time: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.bid_volume: float | None = None
        self.ask_volume: float | None = None
        self.last_price: float | None = None
        self.last_volume: float | None = None
        self.all_data: dict[str, Any] | None = None

    def init_data(self) -> Self:
        raise NotImplementedError("Subclasses must implement init_data")

    def get_all_data(self) -> dict[str, Any]:
        if self.all_data is None:
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "ticker_symbol_name": self.ticker_symbol_name,
                "server_time": self.server_time,
                "bid_price": self.bid_price,
                "ask_price": self.ask_price,
                "bid_volume": self.bid_volume,
                "ask_volume": self.ask_volume,
                "last_price": self.last_price,
                "last_volume": self.last_volume,
            }
        return self.all_data or {}

    def __str__(self) -> str:
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        return str(self.exchange_name)

    def get_local_update_time(self) -> float:
        return float(self.local_update_time)

    def get_symbol_name(self) -> str:
        return str(self.symbol_name)

    def get_ticker_symbol_name(self) -> str | None:
        return self.ticker_symbol_name

    def get_asset_type(self) -> str:
        return str(self.asset_type)

    def get_server_time(self) -> float | None:
        return self.server_time

    def get_bid_price(self) -> float | None:
        return self.bid_price

    def get_ask_price(self) -> float | None:
        return self.ask_price

    def get_bid_volume(self) -> float | None:
        return self.bid_volume

    def get_ask_volume(self) -> float | None:
        return self.ask_volume

    def get_last_price(self) -> float | None:
        return self.last_price

    def get_last_volume(self) -> float | None:
        return self.last_volume


class KuCoinRequestTickerData(KuCoinTickerData):
    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            if isinstance(self.ticker_info, str):
                self.ticker_data = json.loads(self.ticker_info)
            else:
                self.ticker_data = self.ticker_info
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        data = (self.ticker_data or {}).get("data", {})
        self.ticker_symbol_name = self.symbol_name
        self.server_time = from_dict_get_float(data, "time")
        self.last_price = from_dict_get_float(data, "price")
        self.last_volume = from_dict_get_float(data, "size")
        self.bid_price = from_dict_get_float(data, "bestBid")
        self.bid_volume = from_dict_get_float(data, "bestBidSize")
        self.ask_price = from_dict_get_float(data, "bestAsk")
        self.ask_volume = from_dict_get_float(data, "bestAskSize")
        self.has_been_init_data = True
        return self


class KuCoinWssTickerData(KuCoinTickerData):
    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.ticker_data = json.loads(self.ticker_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        data = (self.ticker_data or {}).get("data", {})
        self.ticker_symbol_name = self.symbol_name
        self.server_time = from_dict_get_float(data, "time")
        self.last_price = from_dict_get_float(data, "price")
        self.last_volume = from_dict_get_float(data, "size")
        self.bid_price = from_dict_get_float(data, "bestBid")
        self.bid_volume = from_dict_get_float(data, "bestBidSize")
        self.ask_price = from_dict_get_float(data, "bestAsk")
        self.ask_volume = from_dict_get_float(data, "bestAskSize")
        self.has_been_init_data = True
        return self


class KuCoinStatsTickerData(KuCoinTickerData):
    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.ticker_data = json.loads(self.ticker_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        data = (self.ticker_data or {}).get("data", {})
        self.ticker_symbol_name = from_dict_get_string(data, "symbol")
        self.server_time = from_dict_get_float(data, "time")
        self.last_price = from_dict_get_float(data, "last")
        self.last_volume = from_dict_get_float(data, "vol")
        self.bid_price = from_dict_get_float(data, "buy")
        self.ask_price = from_dict_get_float(data, "sell")
        self.bid_volume = None
        self.ask_volume = None
        self.has_been_init_data = True
        return self
