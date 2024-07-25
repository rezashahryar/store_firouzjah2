import random
import requests
import json

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from core.models import OtpRequest

# create your serializers here


class RequestSendOtpSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    otp_code = serializers.CharField(read_only=True)
    mobile = serializers.CharField()

    def save(self, **kwargs):
        req_otp = OtpRequest.objects.create(
            mobile=self._validated_data['mobile'],
            otp_code=self._random_code()
        )
        req_otp.save()

        request_headers = {
        "accept": "application/json",
        "content-type": "application/json",
        }

        data = {
            "UserName": settings.WEB_SERVICE_OTP_USERNAME,
            "Password": settings.WEB_SERVICE_OTP_PASSWORD,
            "From": settings.SEND_OTP_CODE_FROM,
            "To": req_otp.mobile,
            "Message": f"کد تایید : {req_otp.otp_code} \n انقضاء: {req_otp.valid_until.time().hour}:{req_otp.valid_until.time().minute}:{req_otp.valid_until.time().second}",
        }

        res = requests.post(
            url='https://webone-sms.ir/SMSInOutBox/Send',
            data=json.dumps(data),
            headers=request_headers
        )

        return req_otp
    
    def _random_code(self):
        return int(random.randint(10000, 99999))
 

class CheckOtpSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    otp_code = serializers.IntegerField()
    mobile = serializers.IntegerField()

    def validate(self, attrs):
        try:
            otp_req = OtpRequest.objects.get(
                id=attrs['id'],
                otp_code=attrs['otp_code']
            )

            if otp_req.valid_until < timezone.now():
                raise serializers.ValidationError("this code expired")
        except OtpRequest.DoesNotExist:
            ...
        

            
        return attrs
