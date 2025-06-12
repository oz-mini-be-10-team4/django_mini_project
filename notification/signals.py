from django.db.models.signals import post_save
from django.dispatch import receiver

from analysis.models import Analysis  # 분석 모델 경로에 맞게 수정

from .models import Notification


@receiver(post_save, sender=Analysis)
def create_analysis_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message="새로운 소비 분석 결과가 생성되었습니다. 그래프를 확인해보세요!",
        )
