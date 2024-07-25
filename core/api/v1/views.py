from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from core.models import OtpRequest

# create your views here


class RequestSendOtpView(generics.CreateAPIView):
    queryset = OtpRequest.objects.all()
    serializer_class = serializers.RequestSendOtpSerializer
