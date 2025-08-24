import requests
from celery import shared_task
from django.conf import settings
from django.urls import reverse
from misago.acl.useracl import get_user_acl
from misago.cache.versions import get_cache_versions
from misago.conf.dynamicsettings import DynamicSettings
from misago.threads.models import Post, Thread
from misago.threads.permissions.threads import can_see_post, can_see_thread
from misago.users.models import AnonymousUser, User

from .settings import COLOR, MUTE_CATEGORIES, NEW_REPLY, NEW_THREAD, WEBHOOK_URL


@shared_task(
    name="discord_notifications.call_webhook",
    autoretry_for=(Post.DoesNotExist,),
    default_retry_delay=settings.MISAGO_NOTIFICATIONS_RETRY_DELAY,
    serializer="json",
)
def call_webhook(reply_id: int):
    if not WEBHOOK_URL:
        return

    post = Post.objects.select_related("poster", "thread", "category").get(id=reply_id)
    post.thread.category = post.category

    if post.category_id in MUTE_CATEGORIES:
        return

    cache_versions = get_cache_versions()
    user_acl = get_user_acl(AnonymousUser(), cache_versions)

    if can_see_thread(user_acl, post.thread) and can_see_post(user_acl, post):
        dynamic_settings = DynamicSettings(cache_versions)
        _send_discord_notification(dynamic_settings, post.thread, post, post.poster)


def _send_discord_notification(
    dynamic_settings: DynamicSettings,
    thread: Thread,
    post: Post,
    poster: User,
):
    forum_address = dynamic_settings.forum_address.rstrip("/")
    if not forum_address:
        return

    object = {
        "author": {
            "name": poster.username,
            "icon_url": forum_address
            + reverse(
                "misago:user-avatar",
                kwargs={"pk": poster.pk, "size": 64},
            ),
        },
        "color": COLOR,
    }

    description_data = {
        "category": post.category.name,
        "thread": thread.title,
    }

    if thread.first_post_id == post.id:
        description_data["url"] = forum_address + reverse(
            "misago:thread", kwargs={"pk": thread.pk, "slug": thread.slug}
        )
        object["description"] = NEW_THREAD % description_data
    else:
        description_data["url"] = forum_address + reverse(
            "misago:thread-post",
            kwargs={"pk": thread.pk, "slug": thread.slug, "post": post.id},
        )
        object["description"] = NEW_REPLY % description_data

    requests.post(WEBHOOK_URL, json={"embeds": [object]})
