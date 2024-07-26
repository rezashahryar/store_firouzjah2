from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# create your urls here

router = DefaultRouter()

router.register('product/list', views.ProductListViewSet, basename='product-list')

urlpatterns = [
    path('', include(router.urls))
]

