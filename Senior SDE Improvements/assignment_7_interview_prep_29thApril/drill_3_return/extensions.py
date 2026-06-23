"""
Drill 3 — Your work goes here.

Goal: master the THREE positions of super() in a wrapped method:
  - super() FIRST, then add checks (post-extension)
  - super() CONDITIONALLY (skip in some cases)
  - PRE-CHECK first, then super() (early reject)

Three subclasses:

1. EmailValidator (post-extension)
     - Call super().validate(value) first
     - If it failed, return its (False, reason) UNCHANGED
     - If it passed, also require "@" and "." in value
     - Return (False, "must contain '@'") or similar if missing

2. SkippableValidator (conditional super)
     - If value is a string starting with "trusted:", return (True, None)
       WITHOUT calling super()
     - Otherwise, return super().validate(value)

3. CompositeValidator (pre-check)
     - If "<script>" is in value, return (False, "unsafe") WITHOUT calling super()
     - Otherwise, return super().validate(value)
     - The unsafe check must run BEFORE super() — order matters

Watch out: SkippableValidator and CompositeValidator both need to handle the
case where `value` might not be a string. Use isinstance() before calling
.startswith() or `in` to avoid TypeErrors. (Or rely on super() to catch
non-strings — your call.)
"""
from validator import Validator


class EmailValidator(Validator):
     def validate(self, value):
          output, error = super().validate(value)

          if not output:
               return (output, None)
          if output and ['@', '.'] in value:
               return (output, None)
          return (False, "must contain '@'")

class SkippableValidator(Validator):
    pass


class CompositeValidator(Validator):
    pass
