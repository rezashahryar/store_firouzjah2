from django.urls import path

from . import views

# create your urls here

app_name = 'core'

urlpatterns = [
    path('send-otp/', views.RequestSendOtpView.as_view(), name='send-otp'),
]
