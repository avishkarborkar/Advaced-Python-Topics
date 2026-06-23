# LEGACY PAYMENT SYSTEM — Read this, understand it, then refactor.
# This code WORKS. But it's unmaintainable.
# Count how many places you'd need to change to add a new payment provider.

import uuid
from datetime import datetime


class PaymentService:
    """
    Handles all payment processing for the platform.
    Supports Stripe, PayPal, and internal ledger.
    """

    def __init__(self):
        self.transaction_log = []
        self.receipts = []
        self.ledger_transactions = []

    def process_payment(self, provider_name, method, amount, currency, user_id, details, max_retries=0):
        """
        Main entry point. Returns a dict with status, transaction_id, error, provider.
        """

        # ---- VALIDATION (duplicated per method type) ----

        if method == "credit_card":
            card_number = details.get("card_number", "")
            expiry = details.get("expiry", "")
            cvv = details.get("cvv", "")

            if not card_number.isdigit() or len(card_number) != 16:
                self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
                return {"status": "validation_error", "transaction_id": None,
                        "error": "Card number must be 16 digits", "provider": provider_name}

            # Check expiry
            try:
                exp_date = datetime.strptime(expiry, "%m/%y")
                if exp_date < datetime.now():
                    self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
                    return {"status": "validation_error", "transaction_id": None,
                            "error": "Card is expired", "provider": provider_name}
            except ValueError:
                self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
                return {"status": "validation_error", "transaction_id": None,
                        "error": "Invalid expiry format", "provider": provider_name}

            if not cvv.isdigit() or len(cvv) != 3:
                self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
                return {"status": "validation_error", "transaction_id": None,
                        "error": "CVV must be 3 digits", "provider": provider_name}
            
        # Line 27-52 is basically being repeated again for bank_trasfer, wallet -> Can be a factory
        # _log_transaction is a dict which is not maintainable -> Can be a file of its own.
        # In each paymetn type there is a validation hapenning, it can be enforeced as maybe observer pattern 
        # Line 90-108 -> Processing is basically if/elses which can be againt a factory. and it has 3 functions defined in the base class
        # can simply be a file of its own.
        # Also becasue there are such strict guidelines on validation they can be put into a data class


        elif method == "bank_transfer":
            account = details.get("account_number", "")
            routing = details.get("routing_number", "")

            if not account.isdigit() or not (8 <= len(account) <= 12):
                self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
                return {"status": "validation_error", "transaction_id": None,
                        "error": "Account number must be 8-12 digits", "provider": provider_name}

            if not routing.isdigit() or len(routing) != 9:
                self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
                return {"status": "validation_error", "transaction_id": None,
                        "error": "Routing number must be 9 digits", "provider": provider_name}

        elif method == "wallet":
            wallet_id = details.get("wallet_id", "")
            balance = details.get("balance", 0)

            if not wallet_id:
                self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
                return {"status": "validation_error", "transaction_id": None,
                        "error": "Wallet ID required", "provider": provider_name}

            if balance < amount:
                self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
                return {"status": "validation_error", "transaction_id": None,
                        "error": "Insufficient wallet balance", "provider": provider_name}
        else:
            return {"status": "validation_error", "transaction_id": None,
                    "error": f"Unknown payment method: {method}", "provider": provider_name}

        # ---- PROCESSING (duplicated per provider) ----

        result = None
        attempts = 0

        while attempts <= max_retries:
            if provider_name == "stripe":
                result = self._process_stripe(method, amount, currency, user_id, details)
            elif provider_name == "paypal":
                result = self._process_paypal(method, amount, currency, user_id, details)
            elif provider_name == "ledger":
                result = self._process_ledger(method, amount, currency, user_id, details)
            else:
                return {"status": "failed", "transaction_id": None,
                        "error": f"Unknown provider: {provider_name}", "provider": provider_name}

            if result["status"] == "success":
                break
            attempts += 1

        # ---- LOGGING (same code block every time) ----

        self._log_transaction(provider_name, user_id, amount, currency,
                              result["status"], result.get("transaction_id"))

        # ---- RECEIPTS (only on success) ----

        if result["status"] == "success":
            self.receipts.append({
                "user_id": user_id,
                "amount": amount,
                "currency": currency,
                "status": "success",
                "transaction_id": result["transaction_id"],
                "provider": provider_name,
                "timestamp": datetime.now().isoformat()
            })

        return result

    def _process_stripe(self, method, amount, currency, user_id, details):
        """Simulate Stripe processing."""
        if method not in ("credit_card", "bank_transfer"):
            return {"status": "failed", "transaction_id": None,
                    "error": "Stripe does not support this method", "provider": "stripe"}

        if amount > 10000:
            return {"status": "failed", "transaction_id": None,
                    "error": "Amount exceeds Stripe limit", "provider": "stripe"}

        txn_id = f"stripe_txn_{uuid.uuid4().hex[:8]}"
        return {"status": "success", "transaction_id": txn_id,
                "error": None, "provider": "stripe"}

    def _process_paypal(self, method, amount, currency, user_id, details):
        """Simulate PayPal processing."""
        if method not in ("credit_card", "wallet"):
            return {"status": "failed", "transaction_id": None,
                    "error": "PayPal does not support this method", "provider": "paypal"}

        if currency != "USD":
            return {"status": "failed", "transaction_id": None,
                    "error": "PayPal only supports USD", "provider": "paypal"}

        txn_id = f"pp_txn_{uuid.uuid4().hex[:8]}"
        return {"status": "success", "transaction_id": txn_id,
                "error": None, "provider": "paypal"}

    def _process_ledger(self, method, amount, currency, user_id, details):
        """Simulate internal ledger processing via the legacy system."""
        # Convert dollars to cents
        cents = int(amount * 100)

        # The legacy ledger uses callbacks — we simulate it synchronously here
        result_holder = {}

        def callback(success, ref_code):
            result_holder["success"] = success
            result_holder["ref_code"] = ref_code

        # In the real system this would call LegacyLedger.post_transaction
        # Here we simulate it
        ref_code = f"ledger_ref_{uuid.uuid4().hex[:8]}"
        callback(True, ref_code)

        self.ledger_transactions.append({
            "type": "DEBIT",
            "account": user_id,
            "cents": cents,
            "ref": result_holder["ref_code"]
        })

        if result_holder.get("success"):
            return {"status": "success", "transaction_id": result_holder["ref_code"],
                    "error": None, "provider": "ledger"}
        else:
            return {"status": "failed", "transaction_id": None,
                    "error": "Ledger transaction failed", "provider": "ledger"}

    def _log_transaction(self, provider, user_id, amount, currency, status, txn_id):
        """Log every transaction attempt."""
        self.transaction_log.append(
            f"[{datetime.now().isoformat()}] {provider} | {user_id} | {amount} {currency} | {status}"
        )

    # ---- QUERY METHODS ----

    def get_receipts(self, user_id=None):
        if user_id:
            return [r for r in self.receipts if r["user_id"] == user_id]
        return self.receipts

    def get_log(self):
        return self.transaction_log


# ===================================================================
# PROBLEMS — Count them. This is your code review checklist.
# ===================================================================
#
# SRP violations:
#   - PaymentService validates, processes, logs, generates receipts
#   - Validation logic for 3 payment methods mixed into one method
#   - Each _process_* method duplicates the result dict structure
#
# OCP violations:
#   - Adding a provider: new elif in process_payment + new _process_* method
#   - Adding a payment method: new elif in validation block
#   - Adding an observer (e.g., fraud detection): must edit process_payment
#
# DRY violations:
#   - Validation error return dict created 8 times with same structure
#   - _log_transaction called in validation AND after processing (same pattern)
#   - Result dict {"status": ..., "transaction_id": ..., "error": ..., "provider": ...}
#     constructed identically in every provider method
#
# DIP violations:
#   - process_payment hardcodes provider names as strings
#   - No abstraction over providers — just if/elif
#
# LSP concerns:
#   - _process_ledger works completely differently (callbacks) but pretends to be same
#
# Missing error handling:
#   - What if amount is negative?
#   - What if currency is empty?
#   - No distinction between "retry-able" and "permanent" failures
#
# Total places to change for adding Razorpay: 8+
# Target after refactor: 1 (create RazorpayProvider, register it)
