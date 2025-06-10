from django.db import models

from accounts.models import Account
from utils.constants import TRANSACTION_METHOD, TRANSACTION_TYPE
from utils.models import TimestampModel


class Transaction(TimestampModel):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    method = models.CharField(max_length=20, choices=TRANSACTION_METHOD)
    transaction_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.account_number} - {self.amount}원"
