from django.urls import path

from .views import AccountCreateView, AccountDeleteView, AccountListView

app_name = "accounts"

urlpatterns = [
    path("", AccountListView.as_view(), name="list"),  # GET /api/accounts/
    path(
        "create/", AccountCreateView.as_view(), name="create"
    ),  # POST /api/accounts/create/
    path(
        "<int:pk>/", AccountDeleteView.as_view(), name="delete"
    ),  # DELETE /api/accounts/{id}/
]
