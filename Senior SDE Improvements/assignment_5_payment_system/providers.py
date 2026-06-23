from abc import ABC, abstractmethod
from payments import PaymentMethod, PaymentRequest, PaymentResult, PaymentStatus
import uuid

class PaymentProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def process(self, request: PaymentRequest) -> PaymentResult:
        pass

    @abstractmethod
    def supports(self, method: PaymentMethod) -> bool:
        pass


class StripeProvider(PaymentProvider):

    @property
    def name(self):
        return "stripe"

    def supports(self, method):
        return method in (PaymentMethod.CREDIT_CARD, PaymentMethod.BANK_TRANSFER)

    def process(self, request):
        transaction_id = f"stripe_txn_{uuid.uuid4().hex[:8]}"
        amount = request.amount

        if amount <= 10000:
            return PaymentResult(status=PaymentStatus.SUCCESS, transaction_id=transaction_id, error_message=None, provider=self.name)

        return PaymentResult(status=PaymentStatus.FAILED, transaction_id=None, error_message="Amount exceeds Stripe limit", provider=self.name)


class PayPalProvider(PaymentProvider):

    @property
    def name(self):
        return "paypal"

    def supports(self, method):
        return method in (PaymentMethod.CREDIT_CARD, PaymentMethod.WALLET)

    def process(self, request):
        currency = request.currency
        transaction_id = f"pp_txn_{uuid.uuid4().hex[:8]}"

        if currency == "USD":
            return PaymentResult(status=PaymentStatus.SUCCESS, transaction_id=transaction_id, error_message=None, provider=self.name)

        return PaymentResult(status=PaymentStatus.FAILED, transaction_id=None, error_message="Payment method only allows USD", provider=self.name)


class ProviderFactory:

    def __init__(self):
        self.supported_providers : list[PaymentProvider] = []

    def register(self, provider: PaymentProvider):
        self.supported_providers.append(provider)
        
    def get_provider(self, method):
        for provider in self.supported_providers:
            if provider.supports(method=method):
                return provider
        
        return None
