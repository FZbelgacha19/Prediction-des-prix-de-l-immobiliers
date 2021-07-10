from django.urls import path
from . import views

app_name = 'immeubles'

urlpatterns = [
    path('', views.immeubles_view, name='immeubles_view'),
]