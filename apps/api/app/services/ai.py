import os
from collections.abc import Sequence

from openai import OpenAI

DEFAULT_MODEL = "gpt-5.6-luna"
SYSTEM_PROMPT = (
    "You are Atman, a personal AI mentor. Be useful, clear, and grounded. "
    "Use the conversation context to give practical answers. Do not claim to "
    "remember information that is not present in the supplied context."
)


def generate_reply(messages: Sequence[dict[str, str]]) -> str:
    """Generate an assistant reply from the persisted conversation history."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=os.getenv("ATMAN_MODEL", DEFAULT_MODEL),
        instructions=SYSTEM_PROMPT,
        input=list(messages),
    )

    reply = response.output_text.strip()
    if not reply:
        raise RuntimeError("OpenAI returned an empty response")
    return reply
