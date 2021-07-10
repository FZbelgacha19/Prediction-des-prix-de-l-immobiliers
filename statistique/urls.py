from django.urls import path
from . import views

app_name = 'statistique'

urlpatterns = [
    path('', views.statistique_view, name='statistique_view'),
]