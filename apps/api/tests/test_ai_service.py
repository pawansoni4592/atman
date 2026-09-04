from unittest.mock import patch


def test_generate_reply_uses_configured_model():
    fake_response = type("Response", (), {"output_text": "Hello from Atman"})()
    captured: dict = {}

    class FakeResponses:
        def create(self, **kwargs):
            captured.update(kwargs)
            return fake_response

    fake_client = type("Client", (), {"responses": FakeResponses()})()

    with patch("app.services.ai.OpenAI", return_value=fake_client), patch.dict(
        "os.environ",
        {"OPENAI_API_KEY": "test-key", "ATMAN_MODEL": "test-model"},
        clear=False,
    ):
        from app.services.ai import generate_reply

        messages = [{"role": "user", "content": "Hello"}]
        assert generate_reply(messages) == "Hello from Atman"

    assert captured["model"] == "test-model"
    assert captured["input"] == messages
    assert "instructions" in captured
