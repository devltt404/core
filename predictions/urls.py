from django.urls import path

from .views import Predictions

urlpatterns = [
    path("", Predictions.as_view(), name="predictions"),
]
