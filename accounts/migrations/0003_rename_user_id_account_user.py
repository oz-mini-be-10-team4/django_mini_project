# Generated by Django 5.2.2 on 2025-06-10 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="account",
            old_name="user_id",
            new_name="user",
        ),
    ]
