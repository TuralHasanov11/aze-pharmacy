
import pusher
from django.conf import settings

notificationClient = pusher.Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_APP_KEY,
    secret=settings.PUSHER_APP_SECRET,
    cluster=settings.PUSHER_APP_CLUSTER,
    ssl=settings.PUSHER_SSL
)


class BroadcastChannel:
    def __init__(self, channel_name, event_name, payload):
        self.dispatch(channel_name, event_name, payload)

    def dispatch(self, channel_name, event_name, payload):
        notificationClient.trigger(channel_name, event_name, payload)