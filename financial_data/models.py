from django.db import models


class DailyStock(models.Model):
    open_price = models.FloatField(null=True)
    close_price = models.FloatField(null=True)
    predicted_close_price = models.FloatField(null=True)
    high_price = models.FloatField(null=True)
    low_price = models.FloatField(null=True)
    volume = models.IntegerField(null=True)
    date = models.DateField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date}"
