from datetime import timedelta

from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .analyzers import Analyzer
from .models import Analysis
from .serializers import AnalysisSerializer


class AnalysisListView(generics.ListAPIView):
    serializer_class = AnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Analysis.objects.filter(user=self.request.user)
        analysis_type = self.request.query_params.get("type")
        if analysis_type:
            queryset = queryset.filter(type=analysis_type.upper())
        return queryset


class RunAnalysisView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        analysis_type = request.data.get("type", "WEEKLY").upper()
        end_date = timezone.now().date()

        if analysis_type == "DAILY":
            start_date = end_date - timedelta(days=1)
        elif analysis_type == "WEEKLY":
            start_date = end_date - timedelta(days=7)
        elif analysis_type == "MONTHLY":
            start_date = end_date - timedelta(days=30)
        elif analysis_type == "YEARLY":
            start_date = end_date - timedelta(days=365)
        else:
            return Response(
                {"detail": f"지원하지 않는 분석 타입입니다: {analysis_type}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        analyzer = Analyzer(
            user=request.user,
            type=analysis_type,
            start_date=start_date,
            end_date=end_date,
        )
        result = analyzer.run()

        if result:
            return Response(
                AnalysisSerializer(result).data, status=status.HTTP_201_CREATED
            )
        return Response(
            {"detail": "분석에 사용할 거래 데이터가 없습니다."},
            status=status.HTTP_204_NO_CONTENT,
        )
