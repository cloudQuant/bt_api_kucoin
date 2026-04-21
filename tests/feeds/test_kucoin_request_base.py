from unittest.mock import AsyncMock
import pytest
from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_kucoin.feeds.live_kucoin.request_base import KuCoinRequestData


def test_kucoin_defaults_exchange_name() -> None:
    request_data = KuCoinRequestData(
        public_key="public-key",
        private_key="secret-key",
        passphrase="passphrase",
    )

    assert request_data.exchange_name == "KUCOIN___SPOT"


async def test_kucoin_async_request_allows_missing_extra_data(monkeypatch) -> None:
    request_data = KuCoinRequestData(
        public_key="public-key",
        private_key="secret-key",
        passphrase="passphrase",
        exchange_name="KUCOIN___SPOT",
    )

    async_request_mock = AsyncMock(return_value={"code": "200000", "data": {"serverTime": 1}})
    monkeypatch.setattr(request_data, "async_http_request", async_request_mock)

    result = await request_data.async_request("GET /api/v1/timestamp")

    assert isinstance(result, RequestData)
    assert result.get_extra_data() == {}
    assert result.get_input_data() == {"code": "200000", "data": {"serverTime": 1}}


def test_kucoin_accepts_api_key_and_api_secret_aliases() -> None:
    request_data = KuCoinRequestData(
        api_key="public-key",
        api_secret="secret-key",
        passphrase="passphrase",
    )

    assert request_data.public_key == "public-key"
    assert request_data.private_key == "secret-key"
