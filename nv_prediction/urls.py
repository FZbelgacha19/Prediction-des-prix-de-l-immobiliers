from django.urls import path
from . import views

app_name = 'nv_prediction'

urlpatterns = [
    path('', views.main_view, name='main'),
    path('district/', views.district_view, name='district'),
]