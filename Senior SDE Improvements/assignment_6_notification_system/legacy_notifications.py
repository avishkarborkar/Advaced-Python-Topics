# LEGACY NOTIFICATION SYSTEM — Read this, understand it, then refactor.
# This code WORKS. Tests against the legacy behavior pass.
# But every new requirement forces you to edit NotificationService.send()
# and every feature (channels, filters, formatters) is tangled together.
#
# Count how many distinct concerns live inside send(). Count how many
# existing lines you'd need to touch to add Discord, or credit-card
# redaction, or per-organization quiet hours. That number is your enemy.

import time

class NotificationService:
    """
    Handles all outbound notifications. Supports email, SMS, Slack.
    Also: quiet hours, dedup, rate limit, priority prefixes, truncation,
    signature append, and retries. All in one method. On purpose —
    this is what the legacy code looks like.
    """

    def __init__(self):
        # Per-channel outbox (for test inspection)
        self.emails_sent = []
        self.sms_sent = []
        self.slack_sent = []

        # Middleware state (smushed together as service-level dicts)
        self.recent_sends = {}           # (user_id, subject) -> timestamp (for dedup)
        self.user_send_log = {}          # user_id -> list of timestamps (for rate limit)

        # Config knobs (hard-coded here — another smell)
        self.quiet_hours = (22, 7)       # 10pm to 7am
        self.dedup_window = 60           # seconds
        self.rate_limit = 5              # per minute
        self.sms_max = 160
        self.truncate_at = 500
        self.signature = "Sent via LegacyNotify"

    def send(self, user_id, channel, subject, body, priority, metadata, max_retries=0):
        """
        One method. Seven concerns. This is what you're replacing.

        channel: "email" | "sms" | "slack"
        priority: "low" | "normal" | "high" | "urgent"
        metadata: dict with "hour" (int) and "timestamp" (int unix seconds)
        """

        # ---- QUIET HOURS FILTER ----
        hour = metadata.get("hour", 12)
        start, end = self.quiet_hours
        in_quiet = (hour >= start or hour < end) if start > end else (start <= hour < end)
        # URGENT bypasses quiet hours, but this logic is embedded here
        if in_quiet and priority != "urgent":
            return {
                "delivered": False,
                "channel": channel,
                "error": "blocked: quiet hours",
                "attempts": 0,
            }

        # ---- DEDUP FILTER ----
        now = metadata.get("timestamp", int(time.time()))
        key = (user_id, subject)
        last = self.recent_sends.get(key)
        if last is not None and (now - last) < self.dedup_window:
            return {
                "delivered": False,
                "channel": channel,
                "error": "blocked: duplicate",
                "attempts": 0,
            }

        # ---- RATE LIMIT FILTER ----
        log = self.user_send_log.setdefault(user_id, [])
        # prune old
        log[:] = [t for t in log if (now - t) < 60]
        if len(log) >= self.rate_limit:
            return {
                "delivered": False,
                "channel": channel,
                "error": "blocked: rate limit",
                "attempts": 0,
            }

        # ---- PRIORITY PREFIX FORMATTER ----
        if priority == "urgent":
            subject = "🚨 " + subject
        elif priority == "high":
            subject = "⚠️ " + subject

        # ---- TRUNCATE FORMATTER ----
        if len(body) > self.truncate_at:
            body = body[: self.truncate_at] + "..."

        # ---- SIGNATURE FORMATTER ----
        body = body + "\n\n-- \n" + self.signature

        # ---- CHANNEL DISPATCH + RETRY ----
        attempts = 0
        delivered = False
        error = None

        while attempts <= max_retries:
            attempts += 1
            if channel == "email":
                if not body.strip():
                    error = "email: empty body"
                else:
                    self.emails_sent.append({"to": user_id, "subject": subject, "body": body})
                    delivered = True
            elif channel == "sms":
                if len(body) > self.sms_max:
                    error = "sms: body too long"
                else:
                    self.sms_sent.append({"to": user_id, "body": body})
                    delivered = True
            elif channel == "slack":
                if not subject.startswith("#"):
                    error = "slack: subject must be a channel name starting with #"
                else:
                    self.slack_sent.append({"channel": subject, "body": body})
                    delivered = True
            else:
                return {
                    "delivered": False,
                    "channel": channel,
                    "error": f"unknown channel: {channel}",
                    "attempts": attempts,
                }

            if delivered:
                # success — update dedup + rate-limit state
                self.recent_sends[key] = now
                log.append(now)
                break

        return {
            "delivered": delivered,
            "channel": channel,
            "error": None if delivered else error,
            "attempts": attempts,
        }


# ===================================================================
# PROBLEMS — Count them. This is your code review checklist.
# ===================================================================
#
# SRP violations:
#   - send() does: filtering, formatting, dispatch, retry, state update
#   - Filter state (recent_sends, user_send_log) lives on the service
#
# OCP violations:
#   - New channel: add elif in dispatch block
#   - New filter: insert code somewhere in the middle of send()
#   - New formatter: insert code somewhere in the middle of send()
#   - New priority level: add elif in prefix section
#
# DRY violations:
#   - Block-result dicts constructed four times with same shape
#   - Each filter has its own "return blocked" structure
#
# Coupling:
#   - send() has to know the ORDER of filters, formatters, channels
#   - Change the order → hunt through the method body
#
# Testing pain:
#   - Can't test "quiet hours logic" without exercising the whole pipeline
#   - Can't test "SMS length check" without sending a real SMS
#   - State mutation (recent_sends, user_send_log) is invisible to callers
#
# Places to change for adding Discord: 3 (elif in dispatch, new attribute, docstring)
# Target after refactor: 1 (create DiscordChannel, register it)
#
# Places to change for adding credit-card redaction: 1 (new formatter block mid-method)
# Target after refactor: 1 (new decorator class, register it) — but cleanly isolated
#
# Places to change for per-organization quiet hours: many (self.quiet_hours is shared)
# Target after refactor: 1 (middleware reads from metadata or injected config)
