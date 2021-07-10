from django.urls import path
from . import views

app_name = "user_profile"   


urlpatterns = [
    path('', views.index_profile, name='index_profile'),
]