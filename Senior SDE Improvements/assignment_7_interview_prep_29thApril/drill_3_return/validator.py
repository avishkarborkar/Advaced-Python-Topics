"""
Drill 3 — base class. DO NOT MODIFY.

Validator is a base class for input validation. The base validates
basic shape (non-empty string, length limit). Subclasses add domain
rules — sometimes BEFORE the base check, sometimes INSTEAD of it.

This drill is about knowing WHEN NOT to call super(), and when to call
it conditionally based on what you've already determined.

The contract: validate(value) returns (is_valid: bool, reason: str | None).
"""


class Validator:
    MAX_LEN = 100

    def validate(self, value: str) -> tuple[bool, str | None]:
        if not isinstance(value, str):
            return (False, "must be a string")
        if not value:
            return (False, "must not be empty")
        if len(value) > self.MAX_LEN:
            return (False, f"must be <= {self.MAX_LEN} chars")
        return (True, None)