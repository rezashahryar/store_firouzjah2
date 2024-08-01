from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# create your urls here

router = DefaultRouter()

router.register('products', views.ProductViewSet, basename='product')


urlpatterns = [
    path('create-base-product/', views.BaseProductCreateApiView.as_view(), name='create_base_product'),
    path('', include(router.urls)),
]

