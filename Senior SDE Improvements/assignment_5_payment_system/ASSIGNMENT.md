# Assignment 5: Payment Processing System — Refactor & Extend

## Difficulty: ★★★★★
## Focus: Factory, Adapter, Observer Patterns — Refactoring Legacy Code

---

## Why Factory Pattern?

The legacy code selects providers and validators using `if/elif` chains keyed on strings like `"stripe"` or `"credit_card"`. Every time you add a new provider or payment method, you must find and edit those chains — that is an OCP violation.

**Factory pattern solves this by inverting control:**

| Legacy approach | Factory approach |
|----------------|-----------------|
| `if provider == "stripe": ...` | `factory.get_provider(method)` |
| Adding Razorpay = edit 8 places | Adding Razorpay = create 1 class + register |
| Caller must know provider names | Caller only knows the payment method |
| Hard to test in isolation | Each provider is independently testable |

**Two factories are used here for different reasons:**

- `ProviderFactory` — uses *registration* (`factory.register(provider)`). Providers self-register, so the factory code never changes when new providers are added. This is the Open/Closed Principle in action.
- `ValidatorFactory` — uses *lookup by method type*. Validators are stable (one per method type), so a simple mapping is enough. The factory still centralises the creation decision so callers don't instantiate validators directly.

**Why not just use `if/elif` with imports?**
Because the caller (the processor) would then need to import every provider by name — a hard dependency. With a factory, the processor only depends on the `PaymentProvider` ABC. New providers are plugged in from outside (Dependency Inversion Principle).

**The real senior signal:** knowing *which* kind of factory to use. Registration-based (like `ProviderFactory`) is best when the set of implementations grows over time. Mapping-based (like `ValidatorFactory`) is best when the set is fixed and small.

---

## The Scenario

You've joined a team. They have a **working** payment processing system in `legacy_payments.py` (400+ lines). It handles:

- Processing payments via Stripe, PayPal, and an internal ledger
- Validating credit cards, bank accounts, and wallets
- Logging every transaction
- Sending receipts via email
- Retrying failed payments
- Applying discounts and tax calculations

It works. All tests pass against it. **But it's a nightmare to maintain.**

Your tech lead says:
> "We need to add Razorpay as a payment provider next sprint. Looking at the current code, that means touching 8 different methods. Refactor this so adding a new provider is a one-file change."

---

## What You're Given

| File | What It Is |
|------|-----------|
| `legacy_payments.py` | The ugly working code (~400 lines). **Read this carefully.** |
| `test_payments.py` | Tests for your clean version. **DO NOT MODIFY.** |

## What You Create

| File | Responsibility |
|------|---------------|
| `payments.py` | Payment data classes (amount, currency, method, result) |
| `validators.py` | Validation logic per payment method (card, bank, wallet) |
| `providers.py` | Payment provider implementations (Stripe, PayPal, Ledger) + Factory |
| `adapters.py` | Adapter for the `LegacyLedger` system that can't be changed |
| `processing.py` | `PaymentProcessor` — the orchestrator with retry logic |
| `receipts.py` | Receipt generation + observer for transaction events |

---

## Why This Is Hard

### 1. You must understand the messy code first
The legacy code works. You can't just guess what it does — you must trace through it, understand the business logic, and preserve it exactly. The tests verify behavior, not structure.

### 2. Error handling is a first-class concern
The messy code swallows errors, returns mixed types (sometimes bool, sometimes dict, sometimes None), and has inconsistent error reporting. Your clean version must have a clear error strategy:
- Validation errors vs provider errors vs system errors
- When to retry vs when to fail immediately
- What to return to the caller

### 3. The Adapter is non-trivial
`LegacyLedger` is a class you CANNOT modify (pretend it's a compiled library). Its interface is completely different from your provider interface — different method names, different parameter types, different return format, AND it uses callbacks instead of return values. Wrapping it cleanly is the hardest part.

### 4. You must make design TRADEOFFS
- Should `PaymentResult` be a dataclass or a full class? Why?
- Should validators be classes or functions? Defend your choice.
- Should retry logic live in the processor or in each provider? Why?
- When is inheritance the wrong choice here?

### 5. The Open/Closed test is real
The tests include adding a **brand new provider** (Razorpay) at test time. If your design requires modifying ANY existing file to support it, you fail.

---

## Architecture Guide

### `payments.py` — Data Objects

```
PaymentMethod: Enum — CREDIT_CARD, BANK_TRANSFER, WALLET
PaymentStatus: Enum — SUCCESS, FAILED, PENDING, VALIDATION_ERROR

PaymentRequest:
    amount: float
    currency: str
    method: PaymentMethod
    user_id: str
    details: dict  (card number, bank account, wallet id, etc.)

PaymentResult:
    status: PaymentStatus
    transaction_id: str | None
    error_message: str | None
    provider: str
```

### `validators.py` — Validation (Factory Pattern)

```
PaymentValidator (ABC):
    validate(request: PaymentRequest) -> tuple[bool, str | None]
    # Returns (is_valid, error_message_or_none)

CreditCardValidator:
    - Card number must be 16 digits
    - Expiry must not be in the past
    - CVV must be 3 digits

BankTransferValidator:
    - Account number must be 8-12 digits
    - Routing number must be 9 digits

WalletValidator:
    - Wallet ID must be non-empty
    - Balance in details must be >= amount

ValidatorFactory:
    get_validator(method: PaymentMethod) -> PaymentValidator
    # Uses a dict mapping: {PaymentMethod.CREDIT_CARD: CreditCardValidator, ...}
    # Returns a new validator instance for the given method
```

**Factory design decisions to defend:**

- `ValidatorFactory` uses a static mapping (dict) rather than registration, because the set of payment methods is fixed and known upfront — no runtime extensibility needed here.
- The factory is still valuable even as a simple dict wrapper: it gives you one place to swap validator implementations (e.g., swap in `StrictCreditCardValidator` for a specific region) without touching any call sites.
- Callers (the processor) never import `CreditCardValidator` directly — they ask the factory. This is DIP applied at the validator level.

**Senior decision:** Validators are classes (not functions) because they might need configuration later (e.g., different card rules per country). This is OCP thinking.

### `providers.py` — Payment Providers (Factory + DIP)

```
PaymentProvider (ABC):
    name: str (property)
    process(request: PaymentRequest) -> PaymentResult
    supports(method: PaymentMethod) -> bool

StripeProvider:
    - Supports CREDIT_CARD and BANK_TRANSFER
    - Generates transaction IDs like "stripe_txn_<uuid>"
    - Fails if amount > 10000 (simulate limit)

PayPalProvider:
    - Supports CREDIT_CARD and WALLET
    - Generates transaction IDs like "pp_txn_<uuid>"
    - Fails if currency != "USD" (simulate restriction)

ProviderFactory:
    register(provider: PaymentProvider)
    get_provider(method: PaymentMethod, **kwargs) -> PaymentProvider
    # Returns first registered provider that supports the method
    # Internally stores a list of providers — iterates and calls supports()
    # No if/elif, no string matching, no knowledge of concrete provider classes
```

**Factory design decisions to defend:**

1. **Registration over hard-coding** — `ProviderFactory` holds a list, not a dict keyed by name. `get_provider` calls `supports()` on each registered provider in order. This means the factory has zero knowledge of which providers exist — it only knows the `PaymentProvider` interface.

2. **`supports()` on the provider, not the factory** — Each provider knows what it supports. The factory just asks. If you put the routing logic in the factory, adding a provider requires editing the factory (OCP violation).

3. **First-match semantics** — `get_provider` returns the first registered provider that supports the method. This gives callers explicit control over priority by controlling registration order.

4. **Returns `None` when no provider matches** — The processor handles the "no provider" case, not the factory. The factory's job is lookup only (SRP).

**Senior decision:** Factory uses registration (not if/elif) so new providers register themselves. Adding Razorpay = create class + register. Zero changes to factory code.

### `adapters.py` — The Hard Part

`LegacyLedger` is provided in the test file. It has this interface:

```python
class LegacyLedger:
    def __init__(self):
        self.transactions = []

    def post_transaction(self, txn_type, account, cents, callback):
        # txn_type: "DEBIT" or "CREDIT"
        # account: string
        # cents: int (not float dollars!)
        # callback: function(success: bool, ref_code: str)
        # Calls callback asynchronously-style with result
```

Problems you must solve in `LegacyLedgerAdapter`:
1. Your interface uses `float` dollars → ledger wants `int` cents
2. Your interface returns `PaymentResult` → ledger uses a callback
3. Your interface uses `PaymentMethod` → ledger uses `"DEBIT"` string
4. Your interface has `PaymentRequest` → ledger wants flat parameters
5. The ledger has no `supports()` method — adapter must define this

### `receipts.py` — Observer Pattern

```
TransactionObserver (ABC):
    on_transaction(request: PaymentRequest, result: PaymentResult)

ReceiptGenerator:
    - Stores receipts as dicts with: user_id, amount, status, transaction_id, timestamp
    - Only generates receipts for SUCCESS transactions

TransactionLogger:
    - Logs ALL transactions (success and failure)
    - Format: "[{timestamp}] {provider} | {user_id} | {amount} {currency} | {status}"
```

### `processing.py` — The Orchestrator

```
PaymentProcessor:
    __init__(provider_factory, validator_factory)  # DI — no hardcoded dependencies
    
    add_observer(observer: TransactionObserver)
    
    process_payment(request: PaymentRequest, max_retries=0) -> PaymentResult:
        1. Validate using validator_factory
        2. Get provider from provider_factory
        3. Process payment
        4. If failed and retries remaining: retry
        5. Notify all observers
        6. Return result
```

**Senior decision:** Retry logic lives in the processor (not providers) because:
- It's a cross-cutting concern
- Different callers might want different retry policies
- Providers should be stateless and simple

---

## Common Senior Interview Questions About This Code

Be ready to answer these:

1. **"Why didn't you use inheritance for the providers instead of an ABC?"**
   → You DID use an ABC. But the key is providers don't share implementation — they share interface. ABC enforces the contract.

2. **"Why is retry logic in the processor and not the provider?"**
   → SRP: providers process payments, the processor orchestrates. Retry is an orchestration concern.

3. **"Why classes for validators instead of simple functions?"**
   → OCP: validator classes can be extended (e.g., regional rules) without changing the factory. Functions would require editing the factory to add parameters.

4. **"How would you add Razorpay?"**
   → Create `RazorpayProvider(PaymentProvider)`, implement `process()` and `supports()`, register it with the factory. Zero changes to existing code.

5. **"What would you change if this were production code?"**
   → Async processing, proper logging framework, database transactions, idempotency keys, webhook handling.

---

## Run Tests

```bash
cd assignment_5_payment_system
conda activate mpet
python -m pytest test_payments.py -v                          # All
python -m pytest test_payments.py::TestPaymentData -v         # Data classes
python -m pytest test_payments.py::TestValidators -v          # Validation
python -m pytest test_payments.py::TestProviders -v           # Providers
python -m pytest test_payments.py::TestAdapter -v             # Legacy adapter
python -m pytest test_payments.py::TestFactory -v             # Factory
python -m pytest test_payments.py::TestProcessor -v           # Orchestrator
python -m pytest test_payments.py::TestObservers -v           # Receipt/Logger
python -m pytest test_payments.py::TestOpenClosed -v          # Extensibility
```

---

## Order of Implementation

1. Read `legacy_payments.py` — trace through 2-3 payment flows
2. Read ALL tests — understand the exact interfaces expected
3. `payments.py` — Enums + dataclasses (5 min)
4. `validators.py` — validator classes + factory (10 min)
5. `providers.py` — factory with registration (15 min)
6. `adapters.py` — the adapter challenge (20 min)
7. `receipts.py` — observer (10 min)
8. `processing.py` — orchestrator with retry (15 min)
9. Green tests

Good luck. Read the legacy code first — understand it before you replace it.
