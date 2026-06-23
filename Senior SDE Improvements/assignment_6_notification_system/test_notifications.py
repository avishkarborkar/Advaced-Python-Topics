"""
Tests for Assignment 6 — Notification Dispatch System
DO NOT MODIFY THIS FILE.

Run with: pytest test_notifications.py -v

These tests are your SPEC. Read them before you write a single line of code.
Every class name, method name, and signature you need is here.
"""
import pytest


# ─────────────────────────────────────────────
# 1. Data Objects
# ─────────────────────────────────────────────

class TestNotificationData:

    def test_priority_enum_members(self):
        from notifications import Priority
        assert Priority.LOW is not None
        assert Priority.NORMAL is not None
        assert Priority.HIGH is not None
        assert Priority.URGENT is not None

    def test_channel_enum_members(self):
        from notifications import Channel
        assert Channel.EMAIL is not None
        assert Channel.SMS is not None
        assert Channel.SLACK is not None

    def test_notification_fields(self):
        from notifications import Notification, Channel, Priority
        n = Notification(
            user_id="u1",
            channel=Channel.EMAIL,
            subject="Hi",
            body="Hello world",
            priority=Priority.NORMAL,
            metadata={"hour": 12, "timestamp": 1000},
        )
        assert n.user_id == "u1"
        assert n.channel == Channel.EMAIL
        assert n.subject == "Hi"
        assert n.body == "Hello world"
        assert n.priority == Priority.NORMAL
        assert n.metadata["hour"] == 12

    def test_delivery_result_success(self):
        from notifications import DeliveryResult, Channel
        r = DeliveryResult(delivered=True, channel=Channel.EMAIL, error=None, attempts=1)
        assert r.delivered is True
        assert r.channel == Channel.EMAIL
        assert r.error is None
        assert r.attempts == 1

    def test_delivery_result_failure(self):
        from notifications import DeliveryResult
        r = DeliveryResult(delivered=False, channel=None, error="blocked: quiet hours", attempts=0)
        assert r.delivered is False
        assert r.channel is None
        assert r.error == "blocked: quiet hours"


# ─────────────────────────────────────────────
# 2. Channels + Factory
# ─────────────────────────────────────────────

def _make_notification(body="Hello", subject="Hi", channel=None, priority=None, hour=12, ts=1000):
    from notifications import Notification, Channel, Priority
    return Notification(
        user_id="u1",
        channel=channel or Channel.EMAIL,
        subject=subject,
        body=body,
        priority=priority or Priority.NORMAL,
        metadata={"hour": hour, "timestamp": ts},
    )


class TestChannels:

    def test_channel_is_abstract(self):
        from channels import NotificationChannel
        with pytest.raises(TypeError):
            NotificationChannel()

    def test_email_channel_name(self):
        from channels import EmailChannel
        assert EmailChannel().name == "email"

    def test_email_channel_sends(self):
        from channels import EmailChannel
        c = EmailChannel()
        ok = c.send(_make_notification(body="hello"))
        assert ok is True
        assert len(c.sent) == 1

    def test_email_channel_fails_on_empty_body(self):
        from channels import EmailChannel
        c = EmailChannel()
        ok = c.send(_make_notification(body=""))
        assert ok is False
        assert len(c.sent) == 0

    def test_sms_channel_name(self):
        from channels import SmsChannel
        assert SmsChannel().name == "sms"

    def test_sms_channel_fails_when_too_long(self):
        from channels import SmsChannel
        c = SmsChannel()
        ok = c.send(_make_notification(body="x" * 200))
        assert ok is False
        assert len(c.sent) == 0

    def test_sms_channel_sends_under_limit(self):
        from channels import SmsChannel
        c = SmsChannel()
        ok = c.send(_make_notification(body="short"))
        assert ok is True
        assert len(c.sent) == 1

    def test_slack_channel_name(self):
        from channels import SlackChannel
        assert SlackChannel().name == "slack"

    def test_slack_channel_requires_channel_prefix(self):
        from channels import SlackChannel
        c = SlackChannel()
        ok = c.send(_make_notification(subject="general"))
        assert ok is False

    def test_slack_channel_accepts_channel_prefix(self):
        from channels import SlackChannel
        c = SlackChannel()
        ok = c.send(_make_notification(subject="#general"))
        assert ok is True

    def test_factory_register_and_lookup(self):
        from channels import ChannelFactory, EmailChannel, SmsChannel
        from notifications import Channel
        f = ChannelFactory()
        email = EmailChannel()
        sms = SmsChannel()
        f.register(Channel.EMAIL, email)
        f.register(Channel.SMS, sms)
        assert f.get_channel(Channel.EMAIL) is email
        assert f.get_channel(Channel.SMS) is sms

    def test_factory_returns_none_for_unregistered(self):
        from channels import ChannelFactory
        from notifications import Channel
        f = ChannelFactory()
        assert f.get_channel(Channel.SLACK) is None


# ─────────────────────────────────────────────
# 3. Middleware (Chain of Responsibility)
# ─────────────────────────────────────────────

class TestMiddleware:

    def test_middleware_is_abstract(self):
        from middleware import NotificationMiddleware
        with pytest.raises(TypeError):
            NotificationMiddleware()

    def test_quiet_hours_blocks_during_window(self):
        from middleware import QuietHoursMiddleware
        m = QuietHoursMiddleware(start_hour=22, end_hour=7)
        allow, reason = m.process(_make_notification(hour=23))
        assert allow is False
        assert "quiet" in reason.lower()

    def test_quiet_hours_allows_outside_window(self):
        from middleware import QuietHoursMiddleware
        m = QuietHoursMiddleware(start_hour=22, end_hour=7)
        allow, reason = m.process(_make_notification(hour=12))
        assert allow is True
        assert reason is None

    def test_quiet_hours_lets_urgent_through(self):
        from middleware import QuietHoursMiddleware
        from notifications import Priority
        m = QuietHoursMiddleware(start_hour=22, end_hour=7)
        allow, _ = m.process(_make_notification(hour=23, priority=Priority.URGENT))
        assert allow is True

    def test_dedup_blocks_repeat_within_window(self):
        from middleware import DedupMiddleware
        m = DedupMiddleware(window_seconds=60)
        n1 = _make_notification(subject="Hi", ts=1000)
        n2 = _make_notification(subject="Hi", ts=1030)  # 30s later
        assert m.process(n1) == (True, None)
        allow, reason = m.process(n2)
        assert allow is False
        assert "duplicate" in reason.lower()

    def test_dedup_allows_after_window(self):
        from middleware import DedupMiddleware
        m = DedupMiddleware(window_seconds=60)
        n1 = _make_notification(subject="Hi", ts=1000)
        n2 = _make_notification(subject="Hi", ts=1100)  # 100s later
        m.process(n1)
        allow, _ = m.process(n2)
        assert allow is True

    def test_rate_limit_blocks_over_threshold(self):
        from middleware import RateLimitMiddleware
        m = RateLimitMiddleware(max_per_minute=3)
        for i in range(3):
            allow, _ = m.process(_make_notification(ts=1000 + i))
            assert allow is True
        allow, reason = m.process(_make_notification(ts=1004))
        assert allow is False
        assert "rate" in reason.lower()

    def test_rate_limit_allows_after_window(self):
        from middleware import RateLimitMiddleware
        m = RateLimitMiddleware(max_per_minute=2)
        m.process(_make_notification(ts=1000))
        m.process(_make_notification(ts=1010))
        # 70s later — outside the 60s window
        allow, _ = m.process(_make_notification(ts=1080))
        assert allow is True

    def test_chain_runs_in_order_and_returns_first_block(self):
        from middleware import MiddlewareChain, QuietHoursMiddleware, DedupMiddleware
        chain = MiddlewareChain()
        chain.add(QuietHoursMiddleware(start_hour=22, end_hour=7))
        chain.add(DedupMiddleware(window_seconds=60))
        # Quiet hours should block first
        allow, reason = chain.run(_make_notification(hour=23, ts=1000))
        assert allow is False
        assert "quiet" in reason.lower()

    def test_chain_passes_when_no_blocks(self):
        from middleware import MiddlewareChain, QuietHoursMiddleware
        chain = MiddlewareChain()
        chain.add(QuietHoursMiddleware(start_hour=22, end_hour=7))
        allow, reason = chain.run(_make_notification(hour=12))
        assert allow is True
        assert reason is None


# ─────────────────────────────────────────────
# 4. Decorators
# ─────────────────────────────────────────────

class TestDecorators:

    def test_decorator_is_abstract(self):
        from decorators import NotificationDecorator
        with pytest.raises(TypeError):
            NotificationDecorator()

    def test_priority_prefix_urgent(self):
        from decorators import PriorityPrefixDecorator
        from notifications import Priority
        d = PriorityPrefixDecorator()
        n = d.apply(_make_notification(subject="Fire", priority=Priority.URGENT))
        assert n.subject.startswith("🚨")
        assert "Fire" in n.subject

    def test_priority_prefix_high(self):
        from decorators import PriorityPrefixDecorator
        from notifications import Priority
        d = PriorityPrefixDecorator()
        n = d.apply(_make_notification(subject="Warn", priority=Priority.HIGH))
        assert n.subject.startswith("⚠️")

    def test_priority_prefix_normal_unchanged(self):
        from decorators import PriorityPrefixDecorator
        from notifications import Priority
        d = PriorityPrefixDecorator()
        n = d.apply(_make_notification(subject="Hi", priority=Priority.NORMAL))
        assert n.subject == "Hi"

    def test_truncate_long_body(self):
        from decorators import TruncateDecorator
        d = TruncateDecorator(max_length=10)
        n = d.apply(_make_notification(body="x" * 100))
        assert n.body.endswith("...")
        assert len(n.body) <= 13  # 10 + "..."

    def test_truncate_short_body_unchanged(self):
        from decorators import TruncateDecorator
        d = TruncateDecorator(max_length=100)
        n = d.apply(_make_notification(body="short"))
        assert n.body == "short"

    def test_signature_appends_signature(self):
        from decorators import SignatureDecorator
        d = SignatureDecorator(signature="Team Acme")
        n = d.apply(_make_notification(body="Hello"))
        assert "Hello" in n.body
        assert "Team Acme" in n.body

    def test_decorator_does_not_mutate_input(self):
        from decorators import PriorityPrefixDecorator
        from notifications import Priority
        d = PriorityPrefixDecorator()
        original = _make_notification(subject="Fire", priority=Priority.URGENT)
        original_subject = original.subject
        d.apply(original)
        assert original.subject == original_subject  # unchanged

    def test_pipeline_applies_in_order(self):
        from decorators import DecoratorPipeline, PriorityPrefixDecorator, SignatureDecorator
        from notifications import Priority
        p = DecoratorPipeline()
        p.add(PriorityPrefixDecorator())
        p.add(SignatureDecorator(signature="Acme"))
        n = p.apply(_make_notification(subject="Go", body="Body", priority=Priority.HIGH))
        assert n.subject.startswith("⚠️")
        assert "Acme" in n.body

    def test_pipeline_empty_is_identity(self):
        from decorators import DecoratorPipeline
        p = DecoratorPipeline()
        n_in = _make_notification(subject="Hi", body="Hello")
        n_out = p.apply(n_in)
        assert n_out.subject == "Hi"
        assert n_out.body == "Hello"


# ─────────────────────────────────────────────
# 5. Dispatcher — Orchestrator
# ─────────────────────────────────────────────

class TestDispatcher:

    def _make_dispatcher(self):
        from channels import ChannelFactory, EmailChannel, SmsChannel, SlackChannel
        from middleware import MiddlewareChain
        from decorators import DecoratorPipeline
        from dispatcher import NotificationDispatcher
        from notifications import Channel

        cf = ChannelFactory()
        cf.register(Channel.EMAIL, EmailChannel())
        cf.register(Channel.SMS, SmsChannel())
        cf.register(Channel.SLACK, SlackChannel())

        return NotificationDispatcher(
            channel_factory=cf,
            middleware_chain=MiddlewareChain(),
            decorator_pipeline=DecoratorPipeline(),
        ), cf

    def test_successful_dispatch(self):
        from notifications import Channel
        proc, cf = self._make_dispatcher()
        result = proc.dispatch(_make_notification(channel=Channel.EMAIL, body="Hi"))
        assert result.delivered is True
        assert result.channel == Channel.EMAIL
        assert result.attempts == 1

    def test_blocked_by_middleware_returns_reason(self):
        from channels import ChannelFactory, EmailChannel
        from middleware import MiddlewareChain, QuietHoursMiddleware
        from decorators import DecoratorPipeline
        from dispatcher import NotificationDispatcher
        from notifications import Channel

        cf = ChannelFactory()
        cf.register(Channel.EMAIL, EmailChannel())
        chain = MiddlewareChain()
        chain.add(QuietHoursMiddleware(start_hour=22, end_hour=7))

        proc = NotificationDispatcher(cf, chain, DecoratorPipeline())
        result = proc.dispatch(_make_notification(channel=Channel.EMAIL, hour=23))
        assert result.delivered is False
        assert "quiet" in result.error.lower()
        assert result.attempts == 0

    def test_no_channel_registered_returns_failure(self):
        from channels import ChannelFactory
        from middleware import MiddlewareChain
        from decorators import DecoratorPipeline
        from dispatcher import NotificationDispatcher
        from notifications import Channel

        cf = ChannelFactory()  # nothing registered
        proc = NotificationDispatcher(cf, MiddlewareChain(), DecoratorPipeline())
        result = proc.dispatch(_make_notification(channel=Channel.EMAIL))
        assert result.delivered is False
        assert result.error is not None

    def test_decorator_pipeline_applied_before_send(self):
        from channels import ChannelFactory, EmailChannel
        from middleware import MiddlewareChain
        from decorators import DecoratorPipeline, PriorityPrefixDecorator
        from dispatcher import NotificationDispatcher
        from notifications import Channel, Priority

        cf = ChannelFactory()
        email = EmailChannel()
        cf.register(Channel.EMAIL, email)
        pipe = DecoratorPipeline()
        pipe.add(PriorityPrefixDecorator())

        proc = NotificationDispatcher(cf, MiddlewareChain(), pipe)
        proc.dispatch(_make_notification(channel=Channel.EMAIL, subject="Fire", priority=Priority.URGENT, body="Body"))

        assert len(email.sent) == 1
        assert email.sent[0]["subject"].startswith("🚨")

    def test_retry_on_failure(self):
        from channels import ChannelFactory, NotificationChannel
        from middleware import MiddlewareChain
        from decorators import DecoratorPipeline
        from dispatcher import NotificationDispatcher
        from notifications import Channel

        class FlakyChannel(NotificationChannel):
            def __init__(self):
                self.attempts = 0
                self.sent = []

            @property
            def name(self):
                return "flaky"

            def send(self, notification):
                self.attempts += 1
                if self.attempts < 3:
                    return False
                self.sent.append(notification)
                return True

        flaky = FlakyChannel()
        cf = ChannelFactory()
        cf.register(Channel.EMAIL, flaky)

        proc = NotificationDispatcher(cf, MiddlewareChain(), DecoratorPipeline())
        result = proc.dispatch(_make_notification(channel=Channel.EMAIL), max_retries=3)

        assert result.delivered is True
        assert result.attempts == 3

    def test_retry_exhausted_returns_failure(self):
        from channels import ChannelFactory, NotificationChannel
        from middleware import MiddlewareChain
        from decorators import DecoratorPipeline
        from dispatcher import NotificationDispatcher
        from notifications import Channel

        class AlwaysFail(NotificationChannel):
            def __init__(self):
                self.sent = []

            @property
            def name(self):
                return "fail"

            def send(self, notification):
                return False

        cf = ChannelFactory()
        cf.register(Channel.EMAIL, AlwaysFail())
        proc = NotificationDispatcher(cf, MiddlewareChain(), DecoratorPipeline())
        result = proc.dispatch(_make_notification(channel=Channel.EMAIL), max_retries=2)

        assert result.delivered is False
        assert result.attempts == 3  # 1 initial + 2 retries


# ─────────────────────────────────────────────
# 6. Open/Closed — Extensibility Tests
# ─────────────────────────────────────────────

class TestOpenClosed:

    def test_add_new_channel_without_changing_existing_code(self):
        """Adding Discord should be a one-class addition."""
        from channels import NotificationChannel, ChannelFactory
        from middleware import MiddlewareChain
        from decorators import DecoratorPipeline
        from dispatcher import NotificationDispatcher
        from notifications import Channel

        class DiscordChannel(NotificationChannel):
            def __init__(self):
                self.sent = []

            @property
            def name(self):
                return "discord"

            def send(self, notification):
                self.sent.append(notification)
                return True

        discord = DiscordChannel()
        cf = ChannelFactory()
        cf.register(Channel.EMAIL, discord)  # reuse EMAIL enum for this test

        proc = NotificationDispatcher(cf, MiddlewareChain(), DecoratorPipeline())
        result = proc.dispatch(_make_notification(channel=Channel.EMAIL))
        assert result.delivered is True
        assert len(discord.sent) == 1

    def test_add_new_middleware_without_changing_existing_code(self):
        """A new filter (e.g., priority-based) plugs in with zero edits to existing files."""
        from middleware import NotificationMiddleware, MiddlewareChain
        from channels import ChannelFactory, EmailChannel
        from decorators import DecoratorPipeline
        from dispatcher import NotificationDispatcher
        from notifications import Channel, Priority

        class LowPriorityFilter(NotificationMiddleware):
            def process(self, notification):
                if notification.priority == Priority.LOW:
                    return (False, "blocked: low priority filtered")
                return (True, None)

        cf = ChannelFactory()
        cf.register(Channel.EMAIL, EmailChannel())
        chain = MiddlewareChain()
        chain.add(LowPriorityFilter())

        proc = NotificationDispatcher(cf, chain, DecoratorPipeline())
        result = proc.dispatch(_make_notification(channel=Channel.EMAIL, priority=Priority.LOW))
        assert result.delivered is False
        assert "low priority" in result.error.lower()

    def test_add_new_decorator_without_changing_existing_code(self):
        """Credit-card redaction as a new decorator — zero edits to existing files."""
        from decorators import NotificationDecorator, DecoratorPipeline
        from middleware import MiddlewareChain
        from channels import ChannelFactory, EmailChannel
        from dispatcher import NotificationDispatcher
        from notifications import Channel, Notification
        import re

        class RedactCardsDecorator(NotificationDecorator):
            def apply(self, notification):
                redacted = re.sub(r"\b\d{16}\b", "[REDACTED]", notification.body)
                return Notification(
                    user_id=notification.user_id,
                    channel=notification.channel,
                    subject=notification.subject,
                    body=redacted,
                    priority=notification.priority,
                    metadata=notification.metadata,
                )

        cf = ChannelFactory()
        email = EmailChannel()
        cf.register(Channel.EMAIL, email)
        pipe = DecoratorPipeline()
        pipe.add(RedactCardsDecorator())

        proc = NotificationDispatcher(cf, MiddlewareChain(), pipe)
        proc.dispatch(_make_notification(
            channel=Channel.EMAIL,
            body="Your card 4111111111111111 was charged",
        ))

        assert len(email.sent) == 1
        assert "4111111111111111" not in email.sent[0]["body"]
        assert "[REDACTED]" in email.sent[0]["body"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
