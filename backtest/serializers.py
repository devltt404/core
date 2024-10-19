from rest_framework import serializers


class BacktestSerializers(serializers.Serializer):
    investment_amount = serializers.FloatField(initial=10000)
    short_term = serializers.IntegerField(
        initial=50, help_text="(days)", label="Short term average"
    )
    long_term = serializers.IntegerField(
        initial=200, help_text="(days)", label="Long term average"
    )
