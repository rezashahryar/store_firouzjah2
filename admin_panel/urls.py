from django.urls import path, include

# create your urls here


app_name = 'admin_panel'

urlpatterns = [
    path('api/v1/', include('admin_panel.api.v1.urls')),
]

