from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from store import models as store_models

from panel import models

from . import serializers
from .permissions import HasStore

# create your views here


class ProfileApiView(generics.RetrieveUpdateAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return models.Profile.objects.get(user_id=user.pk)
    

class BaseProductCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.CreateBaseProductSerializer
    permission_classes = [IsAuthenticated, HasStore]
