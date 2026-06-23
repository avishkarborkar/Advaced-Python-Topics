from abc import ABC, abstractmethod
from payments import PaymentRequest, PaymentMethod
from typing import Tuple
import datetime

class PaymentValidator(ABC):

    @abstractmethod
    def validate(self, request: PaymentRequest) -> Tuple[bool, str|None]:
        pass

class CreditCardValidator(PaymentValidator):
    def validate(self, request):
        card_number = request.details.get("card_number")
        cvv = request.details.get("cvv")
        expiry = request.details.get('expiry')

        if not card_number.isdigit() or len(card_number) != 16:
            #self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
            return (False, "Card number must be 16 digits")
        
        try:
            exp_date = datetime.datetime.strptime(expiry, "%m/%y")
            if exp_date < datetime.datetime.now():
                #self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
                return (False, "Card is expired")
        except ValueError:
            #self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
            return (False, "Invalid expiry format")
        
        if not cvv.isdigit() or len(cvv) != 3:
            #self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
            return (False, "CVV must be 3 digits")

        return (True, None)

class BankTransferValidator(PaymentValidator):

    def validate(self, request):
        account = request.details.get("account_number")
        routing = request.details.get("routing_number")


        if not account.isdigit() or not (8 <= len(account) <= 12):
            #self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
            return (False, "Account number must be 8-12 digits")

        if not routing.isdigit() or len(routing) != 9:
            #self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
            return (False, "Routing number must be 9 digits")
        
        return (True, None)
    
class WalletValidator(PaymentValidator):

    def validate(self, request):
        wallet_id = request.details.get("wallet_id")
        balance = request.details.get("balance")
        amount = request.amount

        if not wallet_id:
            #self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
            return (False, "Wallet ID required")

        if balance < amount:
            #self._log_transaction(provider_name, user_id, amount, currency, "validation_error", None)
            return (False, "Insufficient wallet balance")
        
        return (True, None)
    


# This validator factory is used to reroute the request ot the correct validator
# Without the factory, the processor would do:

# if request.method == PaymentMethod.CREDIT_CARD:
#     validator = CreditCardValidator()
# elif request.method == PaymentMethod.BANK_TRANSFER:
#     validator = BankTransferValidator()
# ...

# but now we can simply validate = ValidatorFactor()
#validator = validate.get_validator(request.method)

class ValidatorFactory:

    _validators = {
        PaymentMethod.BANK_TRANSFER: BankTransferValidator,
        PaymentMethod.WALLET: WalletValidator,
        PaymentMethod.CREDIT_CARD: CreditCardValidator
    }

    def get_validator(self, method):
        return self._validators[method]()
