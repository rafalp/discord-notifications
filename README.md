# Discord Webhook

A Misago plugin that calls a Discord webhook whenever a new thread or reply is posted on your forum.

Only threads and posts visible to guests trigger webhook.


## Installation

Clone this repository into the plugins directory of your Misago installation.

Set up a new webhook in your Discord server. [Here's how](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

If you are using `misago-docker`, add the following to [your `settings_override.py` file](https://github.com/rafalp/misago_docker?tab=readme-ov-file#overriding-configuration):

```python
DISCORD_WEBHOOK = {
    "url": "https://discord.com/api/webhooks/000000000000000/1G-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
}

MISAGO_POSTING_MIDDLEWARES = [
    # Always keep FloodProtectionMiddleware middleware first one
    "misago.threads.api.postingendpoint.floodprotection.FloodProtectionMiddleware",
    "misago.threads.api.postingendpoint.category.CategoryMiddleware",
    "misago.threads.api.postingendpoint.privatethread.PrivateThreadMiddleware",
    "misago.threads.api.postingendpoint.reply.ReplyMiddleware",
    "misago.threads.api.postingendpoint.moderationqueue.ModerationQueueMiddleware",
    "misago.threads.api.postingendpoint.participants.ParticipantsMiddleware",
    "misago.threads.api.postingendpoint.pin.PinMiddleware",
    "misago.threads.api.postingendpoint.close.CloseMiddleware",
    "misago.threads.api.postingendpoint.hide.HideMiddleware",
    "misago.threads.api.postingendpoint.protect.ProtectMiddleware",
    "misago.threads.api.postingendpoint.recordedit.RecordEditMiddleware",
    "misago.threads.api.postingendpoint.updatestats.UpdateStatsMiddleware",
    "misago.threads.api.postingendpoint.syncprivatethreads.SyncPrivateThreadsMiddleware",
    # Always keep SaveChangesMiddleware middleware after all state-changing middlewares
    "misago.threads.api.postingendpoint.savechanges.SaveChangesMiddleware",
    # Those middlewares are last because they don't change app state
    "misago.threads.api.postingendpoint.notifications.NotificationsMiddleware",
    # Plugins
    "discord_webhook.postingmiddleware.DiscordNotificationsMiddleware",
]
```

Then replace the `url` value in `DISCORD_WEBHOOK` with your Discord webhook’s URL.

Rebuild and restart your Misago site:

```
# ./appctl rebuild
```

## Configuration options

The `DISCORD_WEBHOOK` dictionary supports additional options:


### `mute_categories`

List of category IDs to exclude from notifications.


### `color`

An integer representing the color value to use in notifications.


### `new_thread`

A template for the new thread notification message. Defaults to:

```python
"Started **%(thread)s** in **%(category)s**\n\n**[View this thread](%(url)s)**""
```


### `new_reply`

A template for the new reply notification message. Defaults to:

```python
"Replied to **%(thread)s** in **%(category)s**\n\n**[View this reply](%(url)s)**""
```


## Copyright and license

Copyright © 2025 [Rafał Pitoń](http://github.com/rafalp)
This program comes with ABSOLUTELY NO WARRANTY.

This is free software and you are welcome to modify and redistribute it under the conditions described in the license.
For the complete license, refer to LICENSE.rst
