from enum import Enum
from dataclasses import dataclass

class PaymentMethod(Enum):
    WALLET = "Wallet"
    BANK_TRANSFER = "Bank Transfer"
    CREDIT_CARD = "Credit Card"


class PaymentStatus(Enum):
    SUCCESS = "Success" 
    FAILED = "Failed"  
    PENDING = "Pending"  
    VALIDATION_ERROR = "Validation Error" 

@dataclass
class PaymentRequest:
    amount: float
    currency: str
    method: PaymentMethod
    user_id: str
    details: dict # We send the necessary details for the type of payment 

@dataclass
class PaymentResult:
    status: PaymentStatus
    transaction_id: str | None
    error_message: str | None
    provider: str
