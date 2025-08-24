from misago.categories import PRIVATE_THREADS_ROOT_NAME
from misago.threads.api.postingendpoint import PostingEndpoint, PostingMiddleware

from .tasks import call_webhook


class DiscordNotificationsMiddleware(PostingMiddleware):
    def use_this_middleware(self):
        return (
            self.mode != PostingEndpoint.EDIT
            and self.tree_name != PRIVATE_THREADS_ROOT_NAME
        )

    def post_save(self, serializer):
        call_webhook.delay(self.post.id)
