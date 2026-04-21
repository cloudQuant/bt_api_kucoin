"""Tests for exchange_registers/register_kucoin.py."""

from __future__ import annotations

from bt_api_kucoin.registry_registration import register_kucoin


class TestRegisterKucoin:
    """Tests for KuCoin registration module."""

    def test_module_imports(self):
        """Test module can be imported."""
        assert register_kucoin is not None
