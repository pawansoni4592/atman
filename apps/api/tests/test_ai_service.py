from unittest.mock import patch


def test_generate_reply_uses_configured_model():
    fake_response = type("Response", (), {"output_text": "Hello from Atman"})()
    fake_client = type("Client", (), {})()
    fake_client.responses = type("Responses", (), {})()
    fake_client.responses.create = lambda **kwargs: fake_response

    with patch("app.services.ai.OpenAI", return_value=fake_client), patch.dict(
        "os.environ",
        {"OPENAI_API_KEY": "test-key", "ATMAN_MODEL": "test-model"},
        clear=False,
    ):
        from app.services.ai import generate_reply

        assert generate_reply([{"role": "user", "content": "Hello"}]) == "Hello from Atman"
        assert fake_client.responses.create
