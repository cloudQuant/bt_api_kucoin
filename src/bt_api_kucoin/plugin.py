from __future__ import annotations

from bt_api_base.gateway.registrar import GatewayRuntimeRegistrar
from bt_api_base.plugins.protocol import PluginInfo
from bt_api_base.registry import ExchangeRegistry

from bt_api_kucoin import __version__
from bt_api_kucoin.registry_registration import register_kucoin


def register_plugin(
    registry: type[ExchangeRegistry], runtime_factory: type[GatewayRuntimeRegistrar]
) -> PluginInfo:
    register_kucoin(registry)

    return PluginInfo(
        name="bt_api_kucoin",
        version=__version__,
        core_requires=">=0.15,<1.0",
        supported_exchanges=("KUCOIN___SPOT", "KUCOIN___FUTURES"),
        supported_asset_types=("SPOT", "FUTURES"),
    )
