# Legacy 

from payments import PaymentMethod, PaymentRequest, PaymentResult, PaymentStatus
from providers import PaymentProvider

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


class LegacyLedgerAdapter(PaymentProvider):
    def __init__(self, ledger: LegacyLedger):
        self.ledger = ledger
    
    @property
    def name(self):
        return 'ledger'
    
    def supports(self, method):
        return method in (PaymentMethod.CREDIT_CARD, PaymentMethod.WALLET, PaymentMethod.BANK_TRANSFER)
    
    def process(self, request):
        txn_type = 'DEBIT'
        account = request.user_id
        amount = request.amount
        cents = int(amount*100)

        result_holder = {}
        def callback(success, ref_code):
           result_holder["success"] = success
           result_holder["ref_code"] = ref_code

        self.ledger.post_transaction(txn_type=txn_type, account=account, cents=cents, callback=callback)

        if result_holder["success"]:
            return PaymentResult(PaymentStatus.SUCCESS, result_holder["ref_code"], None, "ledger")
        return PaymentResult(PaymentStatus.FAILED, None, "Ledger transaction failed", "ledger")

# Your interface uses float dollars → ledger wants int cents
# Your interface returns PaymentResult → ledger uses a callback
# Your interface uses PaymentMethod → ledger uses "DEBIT" string
# Your interface has PaymentRequest → ledger wants flat parameters
# The ledger has no supports() method — adapter must define this

