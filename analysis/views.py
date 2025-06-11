from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from .models import Analysis
from .analyzers import Analyzer
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
        start_date = end_date - timedelta(days=7 if analysis_type == "WEEKLY" else 30)

        analyzer = Analyzer(
            user=request.user,
            type=analysis_type,
            start_date=start_date,
            end_date=end_date,
        )
        result = analyzer.run()

        if result:
            return Response(AnalysisSerializer(result).data, status=status.HTTP_201_CREATED)
        return Response({"detail": "분석에 사용할 거래 데이터가 없습니다."}, status=status.HTTP_204_NO_CONTENT)