from __future__ import annotations

from bt_api_base.balance_utils import simple_balance_handler as _kucoin_balance_handler
from bt_api_base.registry import ExchangeRegistry

from bt_api_kucoin.exchange_data.kucoin_exchange_data import (
    KuCoinExchangeDataFutures,
    KuCoinExchangeDataSpot,
)
from bt_api_kucoin.feeds.live_kucoin.futures import KuCoinRequestDataFutures
from bt_api_kucoin.feeds.live_kucoin.spot import KuCoinRequestDataSpot


def register_kucoin(registry: type[ExchangeRegistry]) -> None:
    registry.register_feed("KUCOIN___SPOT", KuCoinRequestDataSpot)
    registry.register_exchange_data("KUCOIN___SPOT", KuCoinExchangeDataSpot)
    registry.register_balance_handler("KUCOIN___SPOT", _kucoin_balance_handler)

    registry.register_feed("KUCOIN___FUTURES", KuCoinRequestDataFutures)
    registry.register_exchange_data("KUCOIN___FUTURES", KuCoinExchangeDataFutures)
    registry.register_balance_handler("KUCOIN___FUTURES", _kucoin_balance_handler)
