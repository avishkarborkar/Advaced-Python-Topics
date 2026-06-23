from abc import ABC, abstractmethod
from notifications import Priority, Notification

class NotificationMiddleware(ABC):

    @abstractmethod
    def process(self, notification: Notification) -> tuple[bool, str | None]:
        pass


class QuietHoursMiddleware(NotificationMiddleware):

    def __init__(self, start_hour: float, end_hour: float):
        self.start_hour = start_hour
        self.end_hour = end_hour

    def process(self, notification: Notification):
        hour = notification.metadata["hour"]

        if self.start_hour <= self.end_hour:
            in_quiet = self.start_hour <= hour < self.end_hour
        else:
            in_quiet = hour >= self.start_hour or hour < self.end_hour

        if in_quiet and notification.priority != Priority.URGENT:
            return False, "quiet hours"
        return True, None

class DedupMiddleware(NotificationMiddleware):

    def __init__(self, window_seconds: int):
        self.window_seconds = window_seconds
        self.last_seen: dict[tuple[str, str], int] = {}

    def process(self, notification: Notification):
        key = (notification.user_id, notification.subject)
        now = notification.metadata["timestamp"]
        last = self.last_seen.get(key)
        if last is not None and (now - last) < self.window_seconds:
            return False, "duplicate"
        self.last_seen[key] = now
        return True, None


class RateLimitMiddleware(NotificationMiddleware):

    def __init__(self, max_per_minute: int):
        self.max_per_minute = max_per_minute
        self.user_log: dict[str, list[int]] = {}

    def process(self, notification: Notification):
        user = notification.user_id
        now = notification.metadata["timestamp"]
        log = self.user_log.setdefault(user, [])
        log[:] = [t for t in log if (now - t) < 60]
        if len(log) >= self.max_per_minute:
            return False, "rate limit exceeded"
        log.append(now)
        return True, None


class MiddlewareChain:

    def __init__(self):
        self.chain = []

    def add(self, middleware: NotificationMiddleware):
        self.chain.append(middleware)

    def run(self, notification: Notification):
        for middleware in self.chain:
            allow, reason = middleware.process(notification)
            if not allow:
                return False, reason
        return True, None
        


