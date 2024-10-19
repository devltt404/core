from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BacktestSerializers
from .utils import execute_backtest


class Backtest(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "backtest_form.html"

    def get(self, request):
        serializer = BacktestSerializers()
        return Response({"serializer": serializer})

    def post(self, request):
        serializer = BacktestSerializers(data=request.data)
        if serializer.is_valid():
            result = execute_backtest(**serializer.data)
            return Response({"serializer": serializer, "result": result})

        return Response({"serializer": serializer})
