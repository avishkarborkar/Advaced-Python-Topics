"""
Tests for Drill 3. DO NOT MODIFY.
Run with: pytest test_validator.py -v

Skill drilled: when to short-circuit *before* super(), when to call super()
first and *fail-fast on its result*, and when to add additional checks
*after* super() succeeds.
"""
import pytest
from validator import Validator


# ─────────────────────────────────────────────
# 1. EmailValidator — extend after the base
# ─────────────────────────────────────────────
# Run base checks FIRST. If base fails, return its failure unchanged.
# If base passes, ALSO require an "@" and a "." in the value.

class TestEmailValidator:

    def test_inherits_from_validator(self):
        from extensions import EmailValidator
        assert issubclass(EmailValidator, Validator)

    def test_empty_returns_base_error(self):
        from extensions import EmailValidator
        ok, reason = EmailValidator().validate("")
        assert ok is False
        assert "empty" in reason.lower()  # base's reason, not yours

    def test_non_string_returns_base_error(self):
        from extensions import EmailValidator
        ok, reason = EmailValidator().validate(123)
        assert ok is False
        assert "string" in reason.lower()

    def test_too_long_returns_base_error(self):
        from extensions import EmailValidator
        ok, reason = EmailValidator().validate("a" * 101)
        assert ok is False
        # base failure should be returned BEFORE you even check for "@"
        assert "<=" in reason or "100" in reason

    def test_missing_at_sign(self):
        from extensions import EmailValidator
        ok, reason = EmailValidator().validate("alicedomain.com")
        assert ok is False
        assert "@" in reason

    def test_missing_dot(self):
        from extensions import EmailValidator
        ok, reason = EmailValidator().validate("alice@domain")
        assert ok is False
        assert "." in reason or "domain" in reason.lower()

    def test_valid_email(self):
        from extensions import EmailValidator
        ok, reason = EmailValidator().validate("alice@domain.com")
        assert ok is True
        assert reason is None


# ─────────────────────────────────────────────
# 2. SkippableValidator — conditional super
# ─────────────────────────────────────────────
# If `value` starts with "trusted:", skip ALL base validation and accept it.
# Otherwise, defer to super().

class TestSkippableValidator:

    def test_inherits_from_validator(self):
        from extensions import SkippableValidator
        assert issubclass(SkippableValidator, Validator)

    def test_trusted_prefix_skips_base(self):
        """Even though "" would normally fail base checks, with the prefix it passes."""
        from extensions import SkippableValidator
        ok, reason = SkippableValidator().validate("trusted:")
        assert ok is True
        assert reason is None

    def test_trusted_prefix_skips_length_check(self):
        """An over-long string with the prefix should still pass."""
        from extensions import SkippableValidator
        ok, _ = SkippableValidator().validate("trusted:" + "x" * 200)
        assert ok is True

    def test_no_prefix_falls_through(self):
        from extensions import SkippableValidator
        ok, reason = SkippableValidator().validate("regular value")
        assert ok is True
        assert reason is None

    def test_no_prefix_still_runs_base(self):
        """Without prefix, base rules apply."""
        from extensions import SkippableValidator
        ok, reason = SkippableValidator().validate("")
        assert ok is False
        assert "empty" in reason.lower()


# ─────────────────────────────────────────────
# 3. CompositeValidator — pre-check, then super
# ─────────────────────────────────────────────
# Reject anything containing the substring "<script>" with reason "unsafe"
# BEFORE calling super(). Otherwise, defer to super().

class TestCompositeValidator:

    def test_inherits_from_validator(self):
        from extensions import CompositeValidator
        assert issubclass(CompositeValidator, Validator)

    def test_unsafe_short_circuits_before_base(self):
        """Even a 'valid by base rules' string with <script> in it should fail
        with 'unsafe' — your check must run BEFORE super()."""
        from extensions import CompositeValidator
        ok, reason = CompositeValidator().validate("hello <script>alert(1)</script>")
        assert ok is False
        assert "unsafe" in reason.lower()

    def test_unsafe_empty_string_with_script_tag(self):
        """If the string contains <script>, that takes priority — even if it's
        also empty or too long, your 'unsafe' reason should win because you
        checked first."""
        from extensions import CompositeValidator
        # The string IS non-empty and within length here, but also unsafe.
        ok, reason = CompositeValidator().validate("<script>")
        assert ok is False
        assert "unsafe" in reason.lower()

    def test_safe_falls_through_to_base(self):
        from extensions import CompositeValidator
        ok, reason = CompositeValidator().validate("")  # empty → base rejects
        assert ok is False
        assert "empty" in reason.lower()

    def test_safe_valid_passes(self):
        from extensions import CompositeValidator
        ok, reason = CompositeValidator().validate("hello world")
        assert ok is True
        assert reason is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])