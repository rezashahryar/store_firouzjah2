from rest_framework import generics

from . import serializers
from core.models import OtpRequest

# create your views here


class RequestSendOtpView(generics.CreateAPIView):
    queryset = OtpRequest.objects.all()
    serializer_class = serializers.RequestSendOtpSerializer
