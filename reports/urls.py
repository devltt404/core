from django.urls import path

from .views import PerformanceReport

urlpatterns = [
    path("", PerformanceReport.as_view(), name="performance-report"),
]
