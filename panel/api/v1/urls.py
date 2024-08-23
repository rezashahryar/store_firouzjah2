from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# create your urls here

router = DefaultRouter()

router.register('product', views.ProductViewSet, basename='product')
router.register('product-image', views.ProductImageViewSet, basename='product-images')
router.register('shiping-cost', views.ShipingCostViewSet, basename='shiping-cost')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('favorite-products', views.FavoriteProductViewSet, basename='favorite-products')
router.register('lmk-products', views.LetMeKnowProductViewSet, basename='lmk-products')
router.register('support-ticket', views.SupportTicketViewSet, basename='support_ticket')
router.register('answer-support-ticket', views.AnswerSupportTicketViewSet, basename='answer_support_ticket')
router.register('request-photography', views.RequestPhotographyViewSet, basename='request-photography')

urlpatterns = [
    path('profile/', views.ProfileApiView.as_view(), name='profile'),
    path('create/base-product/', views.BaseProductCreateApiView.as_view(), name='create_base_product'),
    path('products-info/', views.ProductsIngoDisplay.as_view(), name='products-info-display'),
    path('order-info/', views.OrderInfoDisplay.as_view(), name='order_info'),
    path('activate-all-products/', views.ActivateAllProducts.as_view(), name='activate_all_products'),
    path('deactivate-all-products/', views.DeActivateAllProducts.as_view(), name='deactivate_all_products'),
    path('', include(router.urls)),
]

