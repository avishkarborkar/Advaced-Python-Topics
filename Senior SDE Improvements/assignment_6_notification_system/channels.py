from abc import ABC, abstractmethod
from notifications import Channel, Notification


class NotificationChannel(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def send(self, notification: Notification) -> bool:
        pass


class EmailChannel(NotificationChannel):

    def __init__(self):
        self.sent = []

    @property
    def name(self):
        return "email"

    def send(self, notification: Notification) -> bool:
        if not notification.body:
            return False
        self.sent.append({"to": notification.user_id, "subject": notification.subject, "body": notification.body})
        return True


class SmsChannel(NotificationChannel):

    def __init__(self):
        self.sent = []

    @property
    def name(self):
        return "sms"

    def send(self, notification: Notification) -> bool:
        if len(notification.body) > 160:
            return False
        self.sent.append({"to": notification.user_id, "subject": notification.subject, "body": notification.body})
        return True


class SlackChannel(NotificationChannel):

    def __init__(self):
        self.sent = []

    @property
    def name(self):
        return "slack"

    def send(self, notification: Notification) -> bool:
        if not notification.subject.startswith("#"):
            return False
        self.sent.append({"channel": notification.subject, "body": notification.body})
        return True


class ChannelFactory:

    def __init__(self):
        self.channels = {}

    def get_channel(self, channel: Channel):
        return self.channels.get(channel)

    def register(self, channel_type: Channel, channel: NotificationChannel):
        self.channels[channel_type] = channel