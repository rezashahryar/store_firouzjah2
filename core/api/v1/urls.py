from django.urls import path

from . import views

# create your urls here

app_name = 'api-v1'

urlpatterns = [
    path('send-otp/', views.RequestSendOtpView.as_view(), name='send-otp'),
    path('check-otp/', views.CheckOtpView.as_view(), name='check-otp'),
]
