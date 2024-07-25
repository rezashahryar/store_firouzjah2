from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

# create your views here


class RequestSendOtpView(generics.GenericAPIView):
    
    def get(self, request):
        return Response("salam")
