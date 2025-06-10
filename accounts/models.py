from django.contrib.auth import get_user_model
from django.db import models

from utils.constants import ACCOUNT_TYPE, BANK_CODES
from utils.models import TimestampModel

User = get_user_model()


class Account(TimestampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    account_number = models.CharField(max_length=30, unique=True)
    bank_code = models.CharField(max_length=3, choices=BANK_CODES)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.user.name} - {self.account_number}"
