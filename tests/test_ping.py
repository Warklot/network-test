import pytest
from ping import HostPinger
from unittest.mock import patch

@pytest.mark.parametrize("host,expected_ping", [
    ("8.8.8.8", 0.05),
    ("1.1.1.1", 0.1),
    ("999.999.999.999", None),
    ("invalid-host", None),
    ("this-host-definitely-does-not-exist-12345.com", None),
])

def test_ping_hosts(host, expected_ping):
    with patch("ping.ping", return_value=expected_ping):
        pinger = HostPinger(host, 1)
        pinger.ping()
        result = pinger.get_info()
        if expected_ping is None:
            assert result["Online"] is False
            assert result["avg_ms"] is None
            assert result["min_ms"] is None
            assert result["max_ms"] is None
        else:
            assert result["Online"] is True
            assert result["avg_ms"] > 0
            assert result["min_ms"] > 0
            assert result["max_ms"] > 0
            assert result["min_ms"] <= result["avg_ms"] <= result["max_ms"]

def test_ping_google_returns_valid_latency():
    with patch("ping.ping", return_value=0.05):
        pinger = HostPinger("8.8.8.8", 2).ping
        pinger.ping()
        result = pinger.get_info()
        assert result["Online"] is True
        assert result["avg_ms"] > 0
        assert result["min_ms"] > 0
        assert result["max_ms"] > 0
        assert result["min_ms"] <= result["avg_ms"] <= result["max_ms"]

def test_ping_offline_has_none_values():
    with patch("ping.ping", return_value=None):
        pinger = HostPinger("10.255.255.1", 1).ping
        pinger.ping()
        result = pinger.get_info()
        assert result["Online"] is False
        assert result["avg_ms"] is None
        assert result["min_ms"] is None
        assert result["max_ms"] is None