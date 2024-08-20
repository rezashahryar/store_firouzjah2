from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# create your urls here

router = DefaultRouter()

router.register('product', views.ProductViewSet, basename='product')
router.register('product-image', views.ProductImageViewSet, basename='product-images')

urlpatterns = [
    path('profile/', views.ProfileApiView.as_view(), name='profile'),
    path('create/base-product/', views.BaseProductCreateApiView.as_view(), name='create_base_product'),
    path('', include(router.urls)),
]

