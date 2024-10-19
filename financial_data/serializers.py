from rest_framework import serializers

from .models import DailyStock


class DailyStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStock
        fields = "__all__"
