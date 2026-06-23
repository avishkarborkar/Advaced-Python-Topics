from providers import ProviderFactory
from validators import ValidatorFactory
from receipts import TransactionObserver
from payments import PaymentRequest, PaymentResult, PaymentStatus


class PaymentProcessor:
    def __init__(self, provider_factory: ProviderFactory, validator_factory: ValidatorFactory):
        self.provider_factory = provider_factory
        self.validator_factory = validator_factory
        self.observers: list[TransactionObserver] = []

    def add_observer(self, observer: TransactionObserver):
        self.observers.append(observer)

    def _notify(self, request: PaymentRequest, result: PaymentResult):
        for obs in self.observers: 
            obs.on_transaction(request, result)

    def process_payment(self, request: PaymentRequest, max_retries: int = 0) -> PaymentResult:
        validator = self.validator_factory.get_validator(request.method)
        is_valid, error = validator.validate(request)
        if not is_valid:
            result = PaymentResult(PaymentStatus.VALIDATION_ERROR, None, error, "")
            self._notify(request, result)
            return result

        provider = self.provider_factory.get_provider(request.method)
        if provider is None:
            result = PaymentResult(PaymentStatus.FAILED, None, "No provider available", "")
            self._notify(request, result)
            return result

        result = provider.process(request)
        attempts = 0
        while result.status != PaymentStatus.SUCCESS and attempts < max_retries:
            result = provider.process(request)
            attempts += 1

        self._notify(request, result)
        return result
