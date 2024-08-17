from itertools import product
from rest_framework import serializers

from panel.models import Profile
from store import models as store_model

# create your serializers here


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['full_name', 'email', 'mobile']
