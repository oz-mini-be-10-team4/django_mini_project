# Generated by Django 5.2.2 on 2025-06-10 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("transaction", "0003_alter_transaction_transaction_at"),
    ]

    operations = [
        migrations.RenameField(
            model_name="transaction",
            old_name="account_id",
            new_name="account",
        ),
    ]
