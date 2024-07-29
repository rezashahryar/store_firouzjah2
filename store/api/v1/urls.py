from django.urls import path, include
from rest_framework_nested import routers

from . import views

# create your urls here

router = routers.DefaultRouter()

router.register('products', views.ProductListViewSet, basename='product-list')
router.register('carts', views.CartViewSet, basename='carts')
router.register('orders', views.OrderViewSet, basename='order')

cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items_router.register('items', views.CartItemViewSet, basename='cart_item')


urlpatterns = [
    path('create/store/', views.CreateStoreApiView.as_view(), name='create-store'),
    path('list/order-dates/', views.OrderDateListApiView.as_view(), name='list-order-dates'),
    path('list/order-times/', views.OrderTimeListApiView.as_view(), name='list-order-times'),
    path('create/product-comment/', views.CreateProductCommentApiView.as_view(), name='create-product-comment'),
    path('create/product-answer-comment/', views.CreateProductAnswerCommentApiView.as_view(), name='create-product-answer-comment'),
    path('', include(router.urls)),
    path('', include(cart_items_router.urls)),
]

