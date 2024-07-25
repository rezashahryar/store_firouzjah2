from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from . import serializers
from core.models import OtpRequest, User

# create your views here


class RequestSendOtpView(generics.CreateAPIView):
    queryset = OtpRequest.objects.all()
    serializer_class = serializers.RequestSendOtpSerializer

    def create(self, request, *args, **kwargs):
        send_otp_serializer = self.serializer_class(data=request.data)
        send_otp_serializer.is_valid(raise_exception=True)
        response_send_otp = send_otp_serializer.save()
        serializer = self.serializer_class(response_send_otp)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckOtpView(generics.GenericAPIView):
    serializer_class = serializers.CheckOtpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = User.objects.get(mobile=serializer.validated_data.get('mobile'))

            if user is not None:
                token = Token.objects.get(user=user)

                try:
                    token = Token.objects.get(user_id=user.id)

                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)

                return Response({
                    "token": str(token)
                })

        except User.DoesNotExist:
            user = User.objects.create(mobile=serializer.validated_data.get('mobile'))
            user.save()
            user.username = f'user_{user.pk}'
            # user.user_permissions.add('web_mail')
            user.save()

            try:
                token = Token.objects.get(user_id=user.id)

            except Token.DoesNotExist:
                token = Token.objects.create(user=user)

            return Response({
                "token": str(token)
            })

        return Response(status=status.HTTP_200_OK)
