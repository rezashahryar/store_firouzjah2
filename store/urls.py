from django.urls import path, include

# create your urls here


app_name = 'store'

urlpatterns = [
    path('api/v1/', include('store.api.v1.urls')),
]

