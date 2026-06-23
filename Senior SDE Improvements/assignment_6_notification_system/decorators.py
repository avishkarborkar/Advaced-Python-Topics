from abc import ABC, abstractmethod
from notifications import Notification, Priority


class NotificationDecorator(ABC):
    @abstractmethod
    def apply(self, notification: Notification) -> Notification:
        pass


class PriorityPrefixDecorator(NotificationDecorator):

    _PREFIXES = {
        Priority.URGENT: "🚨 ",
        Priority.HIGH: "⚠️ ",
        Priority.NORMAL: "",
        Priority.LOW: "",
    }

    def apply(self, notification: Notification) -> Notification:
        prefix = self._PREFIXES.get(notification.priority, "")
        return Notification(
            user_id=notification.user_id,
            channel=notification.channel,
            subject=prefix + notification.subject,
            body=notification.body,
            priority=notification.priority,
            metadata=notification.metadata,
        )


class TruncateDecorator(NotificationDecorator):

    def __init__(self, max_length: int = 500):
        self.max_length = max_length

    def apply(self, notification: Notification) -> Notification:
        body = notification.body
        if len(body) > self.max_length:
            body = body[:self.max_length] + "..."
        return Notification(
            user_id=notification.user_id,
            channel=notification.channel,
            subject=notification.subject,
            body=body,
            priority=notification.priority,
            metadata=notification.metadata,
        )


class SignatureDecorator(NotificationDecorator):

    def __init__(self, signature: str):
        self.signature = signature

    def apply(self, notification: Notification) -> Notification:
        return Notification(
            user_id=notification.user_id,
            channel=notification.channel,
            subject=notification.subject,
            body=notification.body + f"\n\n-- \n{self.signature}",
            priority=notification.priority,
            metadata=notification.metadata,
        )


class DecoratorPipeline:

    def __init__(self):
        self.decorators: list[NotificationDecorator] = []

    def add(self, decorator: NotificationDecorator):
        self.decorators.append(decorator)

    def apply(self, notification: Notification) -> Notification:
        for decorator in self.decorators:
            notification = decorator.apply(notification)
        return notification