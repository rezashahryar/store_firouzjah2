from django.urls import path, include
from rest_framework_nested import routers

from . import views

# create your urls here

router = routers.DefaultRouter()

router.register('products', views.ProductViewSet, basename='product-list')
router.register('carts', views.CartViewSet, basename='carts')
router.register('orders', views.OrderViewSet, basename='order')

cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items_router.register('items', views.CartItemViewSet, basename='cart_item')


urlpatterns = [
    path('categories/', views.CategoryListApiView.as_view(), name='category-list'),
    path('products/category/<int:category_pk>/', views.ProductsOfCategoryListApiView.as_view(), name='products-category'),
    path('contact-us/', views.ContactUsApiView.as_view(), name='contact-us'),
    path('send-report-product/', views.SendReportProduct.as_view(), name='send_report_product'),
    path('same-products/<int:pk>/', views.ListSameProductApiView.as_view(), name='same-products'),
    path('send-request-photography/', views.SendRequestPhotographyApiView.as_view(), name='send-request-photography'),
    path('create/store/', views.CreateStoreApiView.as_view(), name='create-store'),
    path('list/order-dates/', views.OrderDateListApiView.as_view(), name='list-order-dates'),
    path('list/order-times/', views.OrderTimeListApiView.as_view(), name='list-order-times'),
    path('apply/coupon/discount/', views.ApplyCouponDiscount.as_view(), name='coupon'),
    path('create/product-comment/', views.CreateProductCommentApiView.as_view(), name='create-product-comment'),
    path('create/product-answer-comment/', views.CreateProductAnswerCommentApiView.as_view(), name='create-product-answer-comment'),
    path('province/list/', views.ProvinceListApiView.as_view(), name='province_list'),
    path('city/list/<int:province_pk>/', views.CityListApiView.as_view(), name='city_list'),
    path('neighbourhood/list/<int:city_pk>/', views.NeighbourhoodListApiView.as_view(), name='neighbourhood_list'),
    path('', include(router.urls)),
    path('', include(cart_items_router.urls)),
]

