from django.urls import include, path

from .views import DataFetcher

urlpatterns = [
    path("", DataFetcher.as_view(), name="data_fetcher"),
]
