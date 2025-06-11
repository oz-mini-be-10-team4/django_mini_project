from rest_framework import serializers
from .models import Analysis

class AnalysisSerializer(serializers.ModelSerializer):
    result_image = serializers.ImageField(use_url=True)

    class Meta:
        model = Analysis
        fields = (
            "id",
            "about",
            "type",
            "period_start",
            "period_end",
            "description",
            "result_image",
            "created_at",
            "updated_at",
        )
