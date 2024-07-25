from django.urls import path, include

# create your urls here

app_name = 'core'

urlpatterns = [
    path('api/v1/', include('core.api.v1.urls')),
]
