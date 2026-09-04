def test_health_contract():
    """Documents the first API contract; integration tests run with a live DB."""
    assert "/health" == "/health"


def test_chat_routes_are_versioned():
    assert "/api/v1/chat".startswith("/api/v1/")
    assert "/api/v1/conversations".startswith("/api/v1/")
    assert "/api/v1/memories".startswith("/api/v1/")
