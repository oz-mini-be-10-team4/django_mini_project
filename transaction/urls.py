from django.urls import path

from .views import (TransactionCreateView, TransactionDeleteView,
                    TransactionListView, TransactionUpdateView)

app_name = "transaction"

urlpatterns = [
    path("", TransactionListView.as_view(), name="list"),  # GET
    path("create/", TransactionCreateView.as_view(), name="create"),  # POST
    path("<int:pk>/update/", TransactionUpdateView.as_view(), name="update"),  # PATCH
    path("<int:pk>/delete/", TransactionDeleteView.as_view(), name="delete"),  # DELETE
]
