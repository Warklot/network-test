import pytest
from ping import ping_host

@pytest.mark.parametrize("host,expected", [
    ("8.8.8.8", True),
    ("1.1.1.1", True),
    ("999.999.999.999", False),
    ("invalid-host", False),
    ("this-host-definitely-does-not-exist-12345.com", False),
])

def test_ping_hosts(host, expected):
    result = ping_host(host, 1)
    assert result['Online'] == expected

def test_ping_google_returns_valid_latency():
    result = ping_host("8.8.8.8", 2)
    
    assert result['Online'] == True
    assert result['avg_ms'] > 0
    assert result['min_ms'] > 0
    assert result['max_ms'] > 0
    assert result['min_ms'] <= result['avg_ms'] <= result['max_ms']

def test_ping_offline_has_none_values():
    result = ping_host("999.999.999.999", 1)
    
    assert result['Online'] == False
    assert result['avg_ms'] is None
    assert result['min_ms'] is None
    assert result['max_ms'] is None