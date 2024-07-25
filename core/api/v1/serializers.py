from rest_framework import serializers

# create your serializers here


class RequestSendOtpSerializer(serializers.Serializer):
    mobile = serializers.CharField()
