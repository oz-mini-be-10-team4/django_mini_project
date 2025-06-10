from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "id",
            "account_id",
            "amount",
            "balance_after",
            "description",
            "transaction_type",
            "method",
            "transaction_at",
        )
        read_only_fields = ("id",)
