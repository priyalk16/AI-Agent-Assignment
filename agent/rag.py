import json
from pathlib import Path

KB_PATH = Path("data/knowledge_base.json")

with open(KB_PATH, "r", encoding="utf-8") as f:
    KNOWLEDGE_BASE = json.load(f)


def retrieve_knowledge(user_input: str) -> str:
    text = user_input.lower()

    if "pro" in text:
        pro = KNOWLEDGE_BASE["pricing"]["pro"]
        return (
            f"Pro Plan costs {pro['price']}. "
            f"It includes {pro['videos']}, {pro['resolution']} resolution, "
            f"and features like {', '.join(pro['features'])}."
        )

    if "basic" in text:
        basic = KNOWLEDGE_BASE["pricing"]["basic"]
        return (
            f"Basic Plan costs {basic['price']}. "
            f"It includes {basic['videos']} with {basic['resolution']} resolution."
        )

    basic = KNOWLEDGE_BASE["pricing"]["basic"]
    pro = KNOWLEDGE_BASE["pricing"]["pro"]

    return (
        f"We offer two plans:\n"
        f"• Basic: {basic['price']} – {basic['videos']}, {basic['resolution']}\n"
        f"• Pro: {pro['price']} – Unlimited videos, {pro['resolution']}, AI captions, 24/7 support"
    )
