from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

# Swagger 설정
schema_view = get_schema_view(
    openapi.Info(
        title="가계부 API",
        default_version="v1",
        description="팀프로젝트 DRF 기반 가계부 시스템 API 명세서",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # 각 앱의 URL 연결
    path("api/user/", include("user.urls", namespace="user")),
    path("api/accounts/", include("accounts.urls", namespace="accounts")),
    path("api/transactions/", include("transaction.urls", namespace="transaction")),
    # Swagger 문서 경로
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/analysis/", include("analysis.urls", namespace="analysis")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)