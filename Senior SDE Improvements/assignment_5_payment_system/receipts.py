from abc import ABC, abstractmethod
from payments import PaymentRequest, PaymentResult, PaymentStatus
import datetime


class TransactionObserver(ABC):
    @abstractmethod
    def on_transaction(self, request: PaymentRequest, result: PaymentResult):
        pass

class ReceiptGenerator(TransactionObserver):
    def __init__(self):
        self.receipts = []

    def on_transaction(self, request: PaymentRequest, result: PaymentResult):
        if result.status == PaymentStatus.SUCCESS:
            self.receipts.append({
                "user_id": request.user_id,
                "amount": request.amount,
                "status": result.status,
                "transaction_id": result.transaction_id,
                "timestamp": datetime.datetime.now().isoformat()
            })

class TransactionLogger(TransactionObserver):
    def __init__(self):
        self.logs = []

    def on_transaction(self, request: PaymentRequest, result: PaymentResult):
        self.logs.append(f"[{datetime.datetime.now().isoformat()}] {result.provider} | {request.user_id} | {request.amount} {request.currency} | {result.status}")

        