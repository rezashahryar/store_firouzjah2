from django.urls import path, include

from . import views

# create your urls here

urlpatterns = [
    path('profile/', views.ProfileApiView.as_view(), name='profile'),
    # path('create/base-product/', views.BaseProductCreateApiView.as_view(), name='create_base_product'),
]

