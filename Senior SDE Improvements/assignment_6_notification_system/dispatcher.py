from channels import ChannelFactory
from middleware import MiddlewareChain
from decorators import DecoratorPipeline
from notifications import Notification, DeliveryResult


class NotificationDispatcher:

    def __init__(self, channel_factory: ChannelFactory, middleware_chain: MiddlewareChain, decorator_pipeline: DecoratorPipeline):
        self.channel_factory = channel_factory
        self.middleware_chain = middleware_chain
        self.decorator_pipeline = decorator_pipeline

    def dispatch(self, notification: Notification, max_retries: int = 0) -> DeliveryResult:
        allow, reason = self.middleware_chain.run(notification)
        if not allow:
            return DeliveryResult(False, None, reason, 0)

        notification = self.decorator_pipeline.apply(notification)

        channel = self.channel_factory.get_channel(notification.channel)
        if channel is None:
            return DeliveryResult(False, None, "no channel registered", 0)

        delivered = False
        attempts = 0
        for _ in range(max_retries + 1):
            attempts += 1
            if channel.send(notification):
                delivered = True
                break

        return DeliveryResult(delivered, notification.channel, None if delivered else "send failed", attempts)