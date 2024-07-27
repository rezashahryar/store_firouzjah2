from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# create your urls here

router = DefaultRouter()

router.register('products', views.ProductListViewSet, basename='product-list')

urlpatterns = [
    path('create/product-comment/', views.CreateProductCommentApiView.as_view(), name='create-product-comment'),
    path('create/product-answer-comment/', views.CreateProductAnswerCommentApiView.as_view(), name='create-product-answer-comment'),
    path('', include(router.urls)),
]

