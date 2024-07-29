from django.urls import path, include

# create your urls here


app_name = 'user_panel'

urlpatterns = [
    path('api/v1/', include('user_panel.api.v1.urls')),
]

