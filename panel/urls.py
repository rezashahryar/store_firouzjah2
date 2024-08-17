from django.urls import path, include

# create your urls here

app_name = 'panel'

urlpatterns = [
    path('api/v1/', include('panel.api.v1.urls')),
]

