# Generated by Django 5.2.2 on 2025-06-10 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transaction", "0002_rename_transactionhistory_transaction"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="transaction_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
