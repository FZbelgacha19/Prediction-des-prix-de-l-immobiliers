from django.urls import path
from . import views

app_name = 'comparaison'

urlpatterns = [
    path('Les_Donnees', views.Donnees_view, name='Donnees_view'),
    path('Le_Graph', views.Graph_view, name='Graph_view'),
]