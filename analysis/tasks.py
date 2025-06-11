from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from .analyzers import Analyzer

User = get_user_model()


@shared_task
def run_weekly_analysis():
    for user in User.objects.all():
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=7)
        Analyzer(user, type="WEEKLY", start_date=start_date, end_date=end_date).run()


@shared_task
def run_monthly_analysis():
    for user in User.objects.all():
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        Analyzer(user, type="MONTHLY", start_date=start_date, end_date=end_date).run()
