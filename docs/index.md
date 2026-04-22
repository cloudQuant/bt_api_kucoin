# KUCOIN Documentation

## English

Welcome to the KUCOIN documentation for bt_api.

### Quick Start

```bash
pip install bt_api_kucoin
```

```python
from bt_api_py import BtApi

api = BtApi(
    exchange_kwargs={
        "KUCOIN___SPOT": {
            "api_key": "your_key",
            "secret": "your_secret",
        }
    }
)

ticker = api.get_tick("KUCOIN___SPOT", "BTCUSDT")
print(ticker)
```

## 中文

欢迎使用 bt_api 的 KUCOIN 文档。

### 快速开始

```bash
pip install bt_api_kucoin
```

```python
from bt_api_py import BtApi

api = BtApi(
    exchange_kwargs={
        "KUCOIN___SPOT": {
            "api_key": "your_key",
            "secret": "your_secret",
        }
    }
)

ticker = api.get_tick("KUCOIN___SPOT", "BTCUSDT")
print(ticker)
```

## API Reference

See source code in `src/bt_api_kucoin/` for detailed API documentation.
