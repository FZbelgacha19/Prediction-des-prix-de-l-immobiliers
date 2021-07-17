from django.urls import path
from . import views

app_name = 'comparaison'

urlpatterns = [
    path('', views.comparaison_view, name='comparaison_view'),
]