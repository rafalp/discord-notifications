from django.conf import settings


WEBHOOK_URL = None
MUTE_CATEGORIES = set()

COLOR = 0
NEW_THREAD = (
    "Started **%(thread)s** in **%(category)s**" "\n\n**[View this thread](%(url)s)**"
)
NEW_REPLY = (
    "Replied to **%(thread)s** in **%(category)s**" "\n\n**[View this reply](%(url)s)**"
)

DISCORD_WEBHOOK = getattr(settings, "DISCORD_WEBHOOK", None)
if isinstance(DISCORD_WEBHOOK, dict):
    WEBHOOK_URL = DISCORD_WEBHOOK["url"]
    MUTE_CATEGORIES = set(DISCORD_WEBHOOK.get("mute_categories") or [])

    if DISCORD_WEBHOOK.get("color"):
        COLOR = DISCORD_WEBHOOK["color"]
    if DISCORD_WEBHOOK.get("new_thread"):
        NEW_THREAD = DISCORD_WEBHOOK["new_thread"]
    if DISCORD_WEBHOOK.get("new_reply"):
        NEW_REPLY = DISCORD_WEBHOOK["new_reply"]
