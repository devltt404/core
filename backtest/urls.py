from django.urls import path

from .views import Backtest

urlpatterns = [
    path("", Backtest.as_view(), name="backtest"),
]
