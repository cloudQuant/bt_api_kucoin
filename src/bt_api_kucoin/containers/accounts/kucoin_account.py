"""KuCoin account data container."""

from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.accounts.account import AccountData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string

from bt_api_kucoin.containers.balances.kucoin_balance import (
    KuCoinRequestBalanceData,
    KuCoinWssBalanceData,
)


class KuCoinAccountData(AccountData):
    def __init__(
        self,
        account_info: Any,
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(account_info, has_been_json_encoded)
        self.exchange_name = "KUCOIN"
        self.symbol_name = symbol_name
        self.local_update_time = time.time()
        self.asset_type = asset_type
        self.account_data: Any = account_info if has_been_json_encoded else None
        self.server_time: float | None = None
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

        self.account_type: str | None = None

        self.total_balance: float | None = None
        self.available_balance: float | None = None
        self.frozen_balance: float | None = None

        self.currency: str | None = None

    def init_data(self) -> KuCoinAccountData:
        raise NotImplementedError("Subclasses must implement init_data")

    def get_all_data(self) -> dict[str, Any]:
        if self.all_data is None:
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "local_update_time": self.local_update_time,
                "asset_type": self.asset_type,
                "server_time": self.server_time,
                "account_type": self.account_type,
                "currency": self.currency,
                "total_balance": self.total_balance,
                "available_balance": self.available_balance,
                "frozen_balance": self.frozen_balance,
            }
        return self.all_data

    def __str__(self) -> str:
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_local_update_time(self) -> float:
        return self.local_update_time

    def get_symbol_name(self) -> str:
        return self.symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_server_time(self) -> int | float:
        return self.server_time if self.server_time is not None else 0

    def get_account_type(self) -> str:
        return self.account_type if self.account_type is not None else ""

    def get_currency(self) -> str | None:
        return self.currency


class KuCoinRequestAccountData(KuCoinAccountData):
    def init_data(self) -> None:
        if not self.has_been_json_encoded:
            self.account_data = json.loads(self.account_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.account_data, dict) and "data" in self.account_data:
            data = self.account_data["data"]
        else:
            data = self.account_data

        if isinstance(data, list) and len(data) > 0:
            data = data[0]

        self.currency = from_dict_get_string(data, "currency")
        self.account_type = from_dict_get_string(data, "type")
        self.total_balance = from_dict_get_float(data, "balance")
        self.available_balance = from_dict_get_float(data, "available")
        self.frozen_balance = from_dict_get_float(data, "holds")
        self.server_time = time.time() * 1000

        if self.symbol_name == "ALL" and self.currency:
            self.symbol_name = self.currency

        self.has_been_init_data = True
        return self

    def get_balances(self) -> Any:
        if isinstance(self.account_data, dict) and "data" in self.account_data:
            data = self.account_data["data"]
        else:
            data = self.account_data

        if isinstance(data, list):
            return [
                KuCoinRequestBalanceData(
                    json.dumps({"data": acc}),
                    acc.get("currency", self.symbol_name),
                    self.asset_type,
                    True,
                )
                for acc in data
            ]
        else:
            return [KuCoinRequestBalanceData(self.account_info, self.symbol_name, self.asset_type, True)]


class KuCoinWssAccountData(KuCoinAccountData):
    def init_data(self) -> None:
        if not self.has_been_json_encoded:
            self.account_data = json.loads(self.account_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.account_data, dict) and "data" in self.account_data:
            data = self.account_data["data"]
        else:
            data = self.account_data

        self.currency = from_dict_get_string(data, "currency")
        self.account_type = "trade"
        self.total_balance = from_dict_get_float(data, "balance")
        self.available_balance = from_dict_get_float(data, "available")
        self.frozen_balance = from_dict_get_float(data, "holds")
        self.server_time = time.time() * 1000

        if self.symbol_name == "ALL" and self.currency:
            self.symbol_name = self.currency

        self.has_been_init_data = True
        return self

    def get_balances(self) -> Any:
        return [KuCoinWssBalanceData(self.account_info, self.symbol_name, self.asset_type, True)]
