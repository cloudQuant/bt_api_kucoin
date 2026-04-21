"""
KuCoin balance data container.
"""

from __future__ import annotations

import json
import time

from bt_api_base.containers.balances.balance import BalanceData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class KuCoinBalanceData(BalanceData):
    def __init__(self, balance_info, symbol_name, asset_type, has_been_json_encoded=False):
        super().__init__(balance_info, has_been_json_encoded)
        self.exchange_name = "KUCOIN"
        self.symbol_name = symbol_name
        self.local_update_time = time.time()
        self.asset_type = asset_type
        self.balance_data = balance_info if has_been_json_encoded else None
        self.interest = None
        self.unrealized_profit = None
        self.open_order_initial_margin = None
        self.available_margin = None
        self.position_initial_margin = None
        self.used_margin = None
        self.margin = None
        self.server_time = None
        self.all_data = None
        self.has_been_init_data = False

    def init_data(self):
        raise NotImplementedError("Subclasses must implement init_data")

    def get_all_data(self):
        if self.all_data is None:
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "local_update_time": self.local_update_time,
                "asset_type": self.asset_type,
                "interest": self.interest,
                "unrealized_profit": self.unrealized_profit,
                "open_order_initial_margin": self.open_order_initial_margin,
                "available_margin": self.available_margin,
                "position_initial_margin": self.position_initial_margin,
                "used_margin": self.used_margin,
                "margin": self.margin,
                "server_time": self.server_time,
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

    def get_server_time(self):
        return self.server_time

    def get_local_update_time(self):
        return self.local_update_time

    def get_account_id(self):
        return None

    def get_account_type(self):
        return None

    def get_fee_tier(self):
        return None

    def get_max_withdraw_amount(self):
        return None

    def get_margin(self):
        return self.margin

    def get_used_margin(self):
        return self.used_margin

    def get_maintain_margin(self):
        return None

    def get_available_margin(self):
        return self.available_margin

    def get_open_order_initial_margin(self):
        return self.open_order_initial_margin

    def get_position_initial_margin(self):
        return self.position_initial_margin

    def get_unrealized_profit(self):
        return self.unrealized_profit

    def get_interest(self):
        return self.interest


class KuCoinRequestBalanceData(KuCoinBalanceData):
    def init_data(self):
        if not self.has_been_json_encoded:
            self.balance_data = json.loads(self.balance_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.balance_data, dict) and "data" in self.balance_data:
            self.balance_data = self.balance_data["data"]

        if isinstance(self.balance_data, list) and len(self.balance_data) > 0:
            if self.symbol_name and self.symbol_name != "ALL":
                for account in self.balance_data:
                    if account.get("currency") == self.symbol_name:
                        self.balance_data = account
                        break
                else:
                    self.balance_data = self.balance_data[0]
            else:
                self.balance_data = self.balance_data[0]

        self.symbol_name = from_dict_get_string(self.balance_data, "currency")
        self.server_time = time.time() * 1000
        self.margin = from_dict_get_float(self.balance_data, "balance")
        self.available_margin = from_dict_get_float(self.balance_data, "available")
        self.used_margin = from_dict_get_float(self.balance_data, "holds")
        self.open_order_initial_margin = self.used_margin

        self.position_initial_margin = None
        self.unrealized_profit = None
        self.interest = None

        self.has_been_init_data = True
        return self


class KuCoinWssBalanceData(KuCoinBalanceData):
    def init_data(self):
        if not self.has_been_json_encoded:
            self.balance_data = json.loads(self.balance_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.balance_data, dict) and "data" in self.balance_data:
            data = self.balance_data["data"]
        else:
            data = self.balance_data

        self.symbol_name = from_dict_get_string(data, "currency")
        self.server_time = time.time() * 1000
        self.margin = from_dict_get_float(data, "balance")
        self.available_margin = from_dict_get_float(data, "available")
        self.used_margin = from_dict_get_float(data, "holds")
        self.open_order_initial_margin = self.used_margin

        self.position_initial_margin = None
        self.unrealized_profit = None
        self.interest = None

        self.has_been_init_data = True
        return self
