"""
Tests for Assignment 5 — Payment Processing System
DO NOT MODIFY THIS FILE.

Run with: pytest test_payments.py -v
"""
import pytest
import datetime
from unittest.mock import MagicMock


# ─────────────────────────────────────────────
# 1. Payment Data Classes
# ─────────────────────────────────────────────

class TestPaymentData:

    def test_payment_method_enum(self):
        from payments import PaymentMethod
        assert PaymentMethod.CREDIT_CARD is not None
        assert PaymentMethod.BANK_TRANSFER is not None
        assert PaymentMethod.WALLET is not None

    def test_payment_status_enum(self):
        from payments import PaymentStatus
        assert PaymentStatus.SUCCESS is not None
        assert PaymentStatus.FAILED is not None
        assert PaymentStatus.PENDING is not None
        assert PaymentStatus.VALIDATION_ERROR is not None

    def test_payment_request(self):
        from payments import PaymentRequest, PaymentMethod
        req = PaymentRequest(
            amount=99.99,
            currency="USD",
            method=PaymentMethod.CREDIT_CARD,
            user_id="user_123",
            details={"card_number": "4111111111111111", "expiry": "12/28", "cvv": "123"}
        )
        assert req.amount == 99.99
        assert req.currency == "USD"
        assert req.method == PaymentMethod.CREDIT_CARD
        assert req.user_id == "user_123"
        assert req.details["card_number"] == "4111111111111111"

    def test_payment_result(self):
        from payments import PaymentResult, PaymentStatus
        result = PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id="txn_abc123",
            error_message=None,
            provider="stripe"
        )
        assert result.status == PaymentStatus.SUCCESS
        assert result.transaction_id == "txn_abc123"
        assert result.error_message is None
        assert result.provider == "stripe"

    def test_payment_result_failure(self):
        from payments import PaymentResult, PaymentStatus
        result = PaymentResult(
            status=PaymentStatus.FAILED,
            transaction_id=None,
            error_message="Limit exceeded",
            provider="stripe"
        )
        assert result.status == PaymentStatus.FAILED
        assert result.transaction_id is None
        assert result.error_message == "Limit exceeded"


# ─────────────────────────────────────────────
# 2. Validators
# ─────────────────────────────────────────────

class TestValidators:

    def test_validator_is_abstract(self):
        from validators import PaymentValidator
        with pytest.raises(TypeError):
            PaymentValidator()

    def test_credit_card_valid(self):
        from validators import CreditCardValidator
        from payments import PaymentRequest, PaymentMethod
        v = CreditCardValidator()
        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "u1",
                             {"card_number": "4111111111111111", "expiry": "12/28", "cvv": "123"})
        valid, error = v.validate(req)
        assert valid is True
        assert error is None

    def test_credit_card_bad_number(self):
        from validators import CreditCardValidator
        from payments import PaymentRequest, PaymentMethod
        v = CreditCardValidator()
        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "u1",
                             {"card_number": "123", "expiry": "12/28", "cvv": "123"})
        valid, error = v.validate(req)
        assert valid is False
        assert "16 digits" in error

    def test_credit_card_expired(self):
        from validators import CreditCardValidator
        from payments import PaymentRequest, PaymentMethod
        v = CreditCardValidator()
        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "u1",
                             {"card_number": "4111111111111111", "expiry": "01/20", "cvv": "123"})
        valid, error = v.validate(req)
        assert valid is False
        assert "expired" in error.lower()

    def test_credit_card_bad_cvv(self):
        from validators import CreditCardValidator
        from payments import PaymentRequest, PaymentMethod
        v = CreditCardValidator()
        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "u1",
                             {"card_number": "4111111111111111", "expiry": "12/28", "cvv": "12"})
        valid, error = v.validate(req)
        assert valid is False
        assert "CVV" in error or "3 digits" in error

    def test_bank_transfer_valid(self):
        from validators import BankTransferValidator
        from payments import PaymentRequest, PaymentMethod
        v = BankTransferValidator()
        req = PaymentRequest(500, "USD", PaymentMethod.BANK_TRANSFER, "u1",
                             {"account_number": "12345678", "routing_number": "123456789"})
        valid, error = v.validate(req)
        assert valid is True

    def test_bank_transfer_bad_account(self):
        from validators import BankTransferValidator
        from payments import PaymentRequest, PaymentMethod
        v = BankTransferValidator()
        req = PaymentRequest(500, "USD", PaymentMethod.BANK_TRANSFER, "u1",
                             {"account_number": "123", "routing_number": "123456789"})
        valid, error = v.validate(req)
        assert valid is False
        assert "8-12" in error or "account" in error.lower()

    def test_bank_transfer_bad_routing(self):
        from validators import BankTransferValidator
        from payments import PaymentRequest, PaymentMethod
        v = BankTransferValidator()
        req = PaymentRequest(500, "USD", PaymentMethod.BANK_TRANSFER, "u1",
                             {"account_number": "12345678", "routing_number": "123"})
        valid, error = v.validate(req)
        assert valid is False
        assert "9 digits" in error or "routing" in error.lower()

    def test_wallet_valid(self):
        from validators import WalletValidator
        from payments import PaymentRequest, PaymentMethod
        v = WalletValidator()
        req = PaymentRequest(50, "USD", PaymentMethod.WALLET, "u1",
                             {"wallet_id": "wallet_abc", "balance": 100.0})
        valid, error = v.validate(req)
        assert valid is True

    def test_wallet_no_id(self):
        from validators import WalletValidator
        from payments import PaymentRequest, PaymentMethod
        v = WalletValidator()
        req = PaymentRequest(50, "USD", PaymentMethod.WALLET, "u1",
                             {"wallet_id": "", "balance": 100.0})
        valid, error = v.validate(req)
        assert valid is False

    def test_wallet_insufficient_balance(self):
        from validators import WalletValidator
        from payments import PaymentRequest, PaymentMethod
        v = WalletValidator()
        req = PaymentRequest(200, "USD", PaymentMethod.WALLET, "u1",
                             {"wallet_id": "wallet_abc", "balance": 50.0})
        valid, error = v.validate(req)
        assert valid is False
        assert "balance" in error.lower() or "insufficient" in error.lower()

    def test_validator_factory(self):
        from validators import ValidatorFactory, CreditCardValidator, BankTransferValidator, WalletValidator
        from payments import PaymentMethod
        factory = ValidatorFactory()
        assert isinstance(factory.get_validator(PaymentMethod.CREDIT_CARD), CreditCardValidator)
        assert isinstance(factory.get_validator(PaymentMethod.BANK_TRANSFER), BankTransferValidator)
        assert isinstance(factory.get_validator(PaymentMethod.WALLET), WalletValidator)


# ─────────────────────────────────────────────
# 3. Providers
# ─────────────────────────────────────────────

class TestProviders:

    def test_provider_is_abstract(self):
        from providers import PaymentProvider
        with pytest.raises(TypeError):
            PaymentProvider()

    def test_stripe_supports_card(self):
        from providers import StripeProvider
        from payments import PaymentMethod
        p = StripeProvider()
        assert p.supports(PaymentMethod.CREDIT_CARD) is True
        assert p.supports(PaymentMethod.BANK_TRANSFER) is True
        assert p.supports(PaymentMethod.WALLET) is False

    def test_stripe_process_success(self):
        from providers import StripeProvider
        from payments import PaymentRequest, PaymentMethod, PaymentStatus
        p = StripeProvider()
        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "u1",
                             {"card_number": "4111111111111111", "expiry": "12/28", "cvv": "123"})
        result = p.process(req)
        assert result.status == PaymentStatus.SUCCESS
        assert result.transaction_id.startswith("stripe_txn_")
        assert result.provider == "stripe"

    def test_stripe_amount_limit(self):
        from providers import StripeProvider
        from payments import PaymentRequest, PaymentMethod, PaymentStatus
        p = StripeProvider()
        req = PaymentRequest(15000, "USD", PaymentMethod.CREDIT_CARD, "u1",
                             {"card_number": "4111111111111111", "expiry": "12/28", "cvv": "123"})
        result = p.process(req)
        assert result.status == PaymentStatus.FAILED
        assert "limit" in result.error_message.lower()

    def test_paypal_supports_wallet(self):
        from providers import PayPalProvider
        from payments import PaymentMethod
        p = PayPalProvider()
        assert p.supports(PaymentMethod.CREDIT_CARD) is True
        assert p.supports(PaymentMethod.WALLET) is True
        assert p.supports(PaymentMethod.BANK_TRANSFER) is False

    def test_paypal_process_success(self):
        from providers import PayPalProvider
        from payments import PaymentRequest, PaymentMethod, PaymentStatus
        p = PayPalProvider()
        req = PaymentRequest(50, "USD", PaymentMethod.WALLET, "u1",
                             {"wallet_id": "wallet_abc", "balance": 100.0})
        result = p.process(req)
        assert result.status == PaymentStatus.SUCCESS
        assert result.transaction_id.startswith("pp_txn_")

    def test_paypal_non_usd_fails(self):
        from providers import PayPalProvider
        from payments import PaymentRequest, PaymentMethod, PaymentStatus
        p = PayPalProvider()
        req = PaymentRequest(50, "EUR", PaymentMethod.WALLET, "u1",
                             {"wallet_id": "wallet_abc", "balance": 100.0})
        result = p.process(req)
        assert result.status == PaymentStatus.FAILED
        assert "USD" in result.error_message

    def test_provider_name_property(self):
        from providers import StripeProvider, PayPalProvider
        assert StripeProvider().name == "stripe"
        assert PayPalProvider().name == "paypal"


# ─────────────────────────────────────────────
# 4. Adapter
# ─────────────────────────────────────────────

class LegacyLedger:
    """This simulates an external library you CANNOT modify."""

    def __init__(self):
        self.transactions = []

    def post_transaction(self, txn_type, account, cents, callback):
        """
        txn_type: "DEBIT" or "CREDIT"
        account: string
        cents: int (not float dollars!)
        callback: function(success: bool, ref_code: str)
        """
        ref_code = f"ledger_ref_{len(self.transactions) + 1:04d}"
        self.transactions.append({
            "type": txn_type,
            "account": account,
            "cents": cents,
            "ref": ref_code
        })
        callback(True, ref_code)


class TestAdapter:

    def test_adapter_is_a_provider(self):
        from adapters import LegacyLedgerAdapter
        from providers import PaymentProvider
        ledger = LegacyLedger()
        adapter = LegacyLedgerAdapter(ledger)
        assert isinstance(adapter, PaymentProvider)

    def test_adapter_name(self):
        from adapters import LegacyLedgerAdapter
        ledger = LegacyLedger()
        adapter = LegacyLedgerAdapter(ledger)
        assert adapter.name == "ledger"

    def test_adapter_supports_all_methods(self):
        from adapters import LegacyLedgerAdapter
        from payments import PaymentMethod
        ledger = LegacyLedger()
        adapter = LegacyLedgerAdapter(ledger)
        assert adapter.supports(PaymentMethod.CREDIT_CARD) is True
        assert adapter.supports(PaymentMethod.BANK_TRANSFER) is True
        assert adapter.supports(PaymentMethod.WALLET) is True

    def test_adapter_converts_dollars_to_cents(self):
        from adapters import LegacyLedgerAdapter
        from payments import PaymentRequest, PaymentMethod, PaymentStatus
        ledger = LegacyLedger()
        adapter = LegacyLedgerAdapter(ledger)
        req = PaymentRequest(99.99, "USD", PaymentMethod.CREDIT_CARD, "user_42",
                             {"card_number": "4111111111111111"})
        result = adapter.process(req)
        assert result.status == PaymentStatus.SUCCESS
        assert result.transaction_id.startswith("ledger_ref_")
        # Verify the ledger received cents
        assert ledger.transactions[-1]["cents"] == 9999

    def test_adapter_passes_user_as_account(self):
        from adapters import LegacyLedgerAdapter
        from payments import PaymentRequest, PaymentMethod
        ledger = LegacyLedger()
        adapter = LegacyLedgerAdapter(ledger)
        req = PaymentRequest(50, "USD", PaymentMethod.BANK_TRANSFER, "user_77",
                             {"account_number": "12345678", "routing_number": "123456789"})
        adapter.process(req)
        assert ledger.transactions[-1]["account"] == "user_77"
        assert ledger.transactions[-1]["type"] == "DEBIT"

    def test_adapter_handles_failed_callback(self):
        """If the ledger calls back with success=False, adapter returns FAILED."""
        from adapters import LegacyLedgerAdapter
        from payments import PaymentRequest, PaymentMethod, PaymentStatus

        class FailingLedger:
            def __init__(self):
                self.transactions = []
            def post_transaction(self, txn_type, account, cents, callback):
                callback(False, "")

        adapter = LegacyLedgerAdapter(FailingLedger())
        req = PaymentRequest(50, "USD", PaymentMethod.CREDIT_CARD, "u1", {})
        result = adapter.process(req)
        assert result.status == PaymentStatus.FAILED


# ─────────────────────────────────────────────
# 5. Factory with Registration
# ─────────────────────────────────────────────

class TestFactory:

    def test_register_and_get_provider(self):
        from providers import ProviderFactory, StripeProvider
        from payments import PaymentMethod
        factory = ProviderFactory()
        factory.register(StripeProvider())
        provider = factory.get_provider(PaymentMethod.CREDIT_CARD)
        assert provider.name == "stripe"

    def test_get_provider_returns_first_match(self):
        from providers import ProviderFactory, StripeProvider, PayPalProvider
        from payments import PaymentMethod
        factory = ProviderFactory()
        factory.register(StripeProvider())
        factory.register(PayPalProvider())
        # Both support CREDIT_CARD, but Stripe was registered first
        provider = factory.get_provider(PaymentMethod.CREDIT_CARD)
        assert provider.name == "stripe"

    def test_get_provider_falls_through(self):
        from providers import ProviderFactory, StripeProvider, PayPalProvider
        from payments import PaymentMethod
        factory = ProviderFactory()
        factory.register(StripeProvider())
        factory.register(PayPalProvider())
        # Only PayPal supports WALLET
        provider = factory.get_provider(PaymentMethod.WALLET)
        assert provider.name == "paypal"

    def test_get_provider_none_when_unsupported(self):
        from providers import ProviderFactory, StripeProvider
        from payments import PaymentMethod
        factory = ProviderFactory()
        factory.register(StripeProvider())
        provider = factory.get_provider(PaymentMethod.WALLET)
        assert provider is None

    def test_factory_with_adapter(self):
        from providers import ProviderFactory
        from adapters import LegacyLedgerAdapter
        from payments import PaymentMethod
        ledger = LegacyLedger()
        factory = ProviderFactory()
        factory.register(LegacyLedgerAdapter(ledger))
        provider = factory.get_provider(PaymentMethod.WALLET)
        assert provider.name == "ledger"


# ─────────────────────────────────────────────
# 6. Observers
# ─────────────────────────────────────────────

class TestObservers:

    def test_observer_is_abstract(self):
        from receipts import TransactionObserver
        with pytest.raises(TypeError):
            TransactionObserver()

    def test_receipt_generator_on_success(self):
        from receipts import ReceiptGenerator
        from payments import PaymentRequest, PaymentResult, PaymentMethod, PaymentStatus
        gen = ReceiptGenerator()
        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "user_1", {})
        res = PaymentResult(PaymentStatus.SUCCESS, "txn_123", None, "stripe")
        gen.on_transaction(req, res)
        assert len(gen.receipts) == 1
        assert gen.receipts[0]["user_id"] == "user_1"
        assert gen.receipts[0]["amount"] == 100
        assert gen.receipts[0]["transaction_id"] == "txn_123"

    def test_receipt_generator_ignores_failures(self):
        from receipts import ReceiptGenerator
        from payments import PaymentRequest, PaymentResult, PaymentMethod, PaymentStatus
        gen = ReceiptGenerator()
        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "user_1", {})
        res = PaymentResult(PaymentStatus.FAILED, None, "some error", "stripe")
        gen.on_transaction(req, res)
        assert len(gen.receipts) == 0

    def test_transaction_logger_logs_all(self):
        from receipts import TransactionLogger
        from payments import PaymentRequest, PaymentResult, PaymentMethod, PaymentStatus
        logger = TransactionLogger()
        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "user_1", {})

        res_ok = PaymentResult(PaymentStatus.SUCCESS, "txn_1", None, "stripe")
        res_fail = PaymentResult(PaymentStatus.FAILED, None, "error", "paypal")

        logger.on_transaction(req, res_ok)
        logger.on_transaction(req, res_fail)

        assert len(logger.logs) == 2
        assert "stripe" in logger.logs[0]
        assert "user_1" in logger.logs[0]
        assert "100" in logger.logs[0]
        assert "paypal" in logger.logs[1]


# ─────────────────────────────────────────────
# 7. Processor — The Orchestrator
# ─────────────────────────────────────────────

class TestProcessor:

    def _make_processor(self):
        from providers import ProviderFactory, StripeProvider, PayPalProvider
        from validators import ValidatorFactory
        from processing import PaymentProcessor

        pf = ProviderFactory()
        pf.register(StripeProvider())
        pf.register(PayPalProvider())
        vf = ValidatorFactory()
        return PaymentProcessor(provider_factory=pf, validator_factory=vf)

    def test_successful_payment(self):
        from payments import PaymentRequest, PaymentMethod, PaymentStatus
        proc = self._make_processor()
        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "u1",
                             {"card_number": "4111111111111111", "expiry": "12/28", "cvv": "123"})
        result = proc.process_payment(req)
        assert result.status == PaymentStatus.SUCCESS

    def test_validation_failure_returns_validation_error(self):
        from payments import PaymentRequest, PaymentMethod, PaymentStatus
        proc = self._make_processor()
        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "u1",
                             {"card_number": "bad", "expiry": "12/28", "cvv": "123"})
        result = proc.process_payment(req)
        assert result.status == PaymentStatus.VALIDATION_ERROR
        assert result.error_message is not None

    def test_no_provider_returns_failed(self):
        """If no provider supports the method, return FAILED."""
        from payments import PaymentRequest, PaymentMethod, PaymentStatus
        from providers import ProviderFactory
        from validators import ValidatorFactory
        from processing import PaymentProcessor

        # Empty factory — no providers registered
        proc = PaymentProcessor(provider_factory=ProviderFactory(), validator_factory=ValidatorFactory())
        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "u1",
                             {"card_number": "4111111111111111", "expiry": "12/28", "cvv": "123"})
        result = proc.process_payment(req)
        assert result.status == PaymentStatus.FAILED
        assert "provider" in result.error_message.lower() or "no" in result.error_message.lower()

    def test_retry_on_failure(self):
        """Processor retries on provider failure."""
        from payments import PaymentRequest, PaymentResult, PaymentMethod, PaymentStatus
        from providers import PaymentProvider, ProviderFactory
        from validators import ValidatorFactory
        from processing import PaymentProcessor

        class FlakyProvider(PaymentProvider):
            def __init__(self):
                self.attempt = 0

            @property
            def name(self):
                return "flaky"

            def supports(self, method):
                return True

            def process(self, request):
                self.attempt += 1
                if self.attempt < 3:
                    return PaymentResult(PaymentStatus.FAILED, None, "Temporary error", "flaky")
                return PaymentResult(PaymentStatus.SUCCESS, "flaky_txn_1", None, "flaky")

        pf = ProviderFactory()
        pf.register(FlakyProvider())
        proc = PaymentProcessor(provider_factory=pf, validator_factory=ValidatorFactory())

        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "u1",
                             {"card_number": "4111111111111111", "expiry": "12/28", "cvv": "123"})
        result = proc.process_payment(req, max_retries=3)
        assert result.status == PaymentStatus.SUCCESS

    def test_retry_exhausted(self):
        """If all retries fail, return the last failure."""
        from payments import PaymentRequest, PaymentResult, PaymentMethod, PaymentStatus
        from providers import PaymentProvider, ProviderFactory
        from validators import ValidatorFactory
        from processing import PaymentProcessor

        class AlwaysFailProvider(PaymentProvider):
            @property
            def name(self):
                return "fail"

            def supports(self, method):
                return True

            def process(self, request):
                return PaymentResult(PaymentStatus.FAILED, None, "Permanent error", "fail")

        pf = ProviderFactory()
        pf.register(AlwaysFailProvider())
        proc = PaymentProcessor(provider_factory=pf, validator_factory=ValidatorFactory())

        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "u1",
                             {"card_number": "4111111111111111", "expiry": "12/28", "cvv": "123"})
        result = proc.process_payment(req, max_retries=2)
        assert result.status == PaymentStatus.FAILED

    def test_observers_notified(self):
        from payments import PaymentRequest, PaymentMethod, PaymentStatus
        from receipts import ReceiptGenerator, TransactionLogger
        proc = self._make_processor()

        receipt_gen = ReceiptGenerator()
        logger = TransactionLogger()
        proc.add_observer(receipt_gen)
        proc.add_observer(logger)

        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "u1",
                             {"card_number": "4111111111111111", "expiry": "12/28", "cvv": "123"})
        proc.process_payment(req)

        assert len(receipt_gen.receipts) == 1
        assert len(logger.logs) == 1

    def test_observers_notified_on_failure_too(self):
        from payments import PaymentRequest, PaymentMethod, PaymentStatus
        from receipts import ReceiptGenerator, TransactionLogger
        proc = self._make_processor()

        receipt_gen = ReceiptGenerator()
        logger = TransactionLogger()
        proc.add_observer(receipt_gen)
        proc.add_observer(logger)

        # This will fail validation
        req = PaymentRequest(100, "USD", PaymentMethod.CREDIT_CARD, "u1",
                             {"card_number": "bad", "expiry": "12/28", "cvv": "123"})
        proc.process_payment(req)

        assert len(receipt_gen.receipts) == 0  # no receipt for failures
        assert len(logger.logs) == 1  # but logger logs everything


# ─────────────────────────────────────────────
# 8. Open/Closed — The Real Senior Test
# ─────────────────────────────────────────────

class TestOpenClosed:

    def test_add_new_provider_without_changing_existing_code(self):
        """
        This is what the tech lead asked for.
        Adding Razorpay should require ZERO changes to existing files.
        """
        from providers import PaymentProvider, ProviderFactory, StripeProvider
        from validators import ValidatorFactory
        from processing import PaymentProcessor
        from payments import PaymentRequest, PaymentResult, PaymentMethod, PaymentStatus

        # A brand new provider — written at test time, not in any source file
        class RazorpayProvider(PaymentProvider):
            @property
            def name(self):
                return "razorpay"

            def supports(self, method):
                return method in (PaymentMethod.CREDIT_CARD, PaymentMethod.BANK_TRANSFER, PaymentMethod.WALLET)

            def process(self, request):
                if request.amount > 50000:
                    return PaymentResult(PaymentStatus.FAILED, None, "Razorpay limit exceeded", "razorpay")
                return PaymentResult(PaymentStatus.SUCCESS, f"rzp_txn_001", None, "razorpay")

        # Register it — no changes to ProviderFactory, PaymentProcessor, or anything else
        pf = ProviderFactory()
        pf.register(RazorpayProvider())
        vf = ValidatorFactory()
        proc = PaymentProcessor(provider_factory=pf, validator_factory=vf)

        req = PaymentRequest(500, "USD", PaymentMethod.CREDIT_CARD, "u1",
                             {"card_number": "4111111111111111", "expiry": "12/28", "cvv": "123"})
        result = proc.process_payment(req)
        assert result.status == PaymentStatus.SUCCESS
        assert result.provider == "razorpay"

    def test_add_new_observer_without_changing_existing_code(self):
        """New observer types should just work."""
        from receipts import TransactionObserver
        from providers import ProviderFactory, StripeProvider
        from validators import ValidatorFactory
        from processing import PaymentProcessor
        from payments import PaymentRequest, PaymentResult, PaymentMethod, PaymentStatus

        class FraudDetector(TransactionObserver):
            def __init__(self):
                self.flagged = []

            def on_transaction(self, request, result):
                if request.amount > 5000:
                    self.flagged.append(request.user_id)

        pf = ProviderFactory()
        pf.register(StripeProvider())
        vf = ValidatorFactory()
        proc = PaymentProcessor(provider_factory=pf, validator_factory=vf)

        detector = FraudDetector()
        proc.add_observer(detector)

        req = PaymentRequest(7500, "USD", PaymentMethod.CREDIT_CARD, "suspicious_user",
                             {"card_number": "4111111111111111", "expiry": "12/28", "cvv": "123"})
        proc.process_payment(req)
        assert "suspicious_user" in detector.flagged

    def test_adapter_integrates_with_full_pipeline(self):
        """LegacyLedger works through the full processor pipeline."""
        from providers import ProviderFactory
        from adapters import LegacyLedgerAdapter
        from validators import ValidatorFactory
        from processing import PaymentProcessor
        from receipts import ReceiptGenerator
        from payments import PaymentRequest, PaymentMethod, PaymentStatus

        ledger = LegacyLedger()
        pf = ProviderFactory()
        pf.register(LegacyLedgerAdapter(ledger))
        vf = ValidatorFactory()
        proc = PaymentProcessor(provider_factory=pf, validator_factory=vf)

        receipt_gen = ReceiptGenerator()
        proc.add_observer(receipt_gen)

        req = PaymentRequest(250.50, "USD", PaymentMethod.CREDIT_CARD, "user_99",
                             {"card_number": "4111111111111111", "expiry": "12/28", "cvv": "123"})
        result = proc.process_payment(req)

        assert result.status == PaymentStatus.SUCCESS
        assert result.provider == "ledger"
        assert len(ledger.transactions) == 1
        assert ledger.transactions[0]["cents"] == 25050
        assert len(receipt_gen.receipts) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
