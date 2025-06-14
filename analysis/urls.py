from django.urls import path

from .views import AnalysisListView, RunAnalysisView

app_name = "analysis"

urlpatterns = [
    path("list/", AnalysisListView.as_view(), name="list"),
    path("run/", RunAnalysisView.as_view(), name="run"),
]
