# from django.db import models
from .querys import getZoneList, getTypeBien, getEtat
from django import forms
from djongo import models
from django.contrib.auth.models import User
 

class predict(models.Model):
    zone = models.CharField(verbose_name="Zone (adresse)", null=False, choices=getZoneList(),max_length=700)
    typeBien = models.CharField(verbose_name="Type de Bien", null=False, choices=getTypeBien(),max_length=700)
    etat = models.CharField(verbose_name="Etat de logement", null=False, choices=getEtat(),max_length=700)
    nomberEtage = models.IntegerField(
        verbose_name="NB étages à vendre", null=True)
    surface = models.IntegerField(verbose_name="Surface",null=False)

    class Meta:
        abstract = True


class Prediction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    _id = models.ObjectIdField()
    predict = models.EmbeddedField(
        model_container=predict
    )
    price = models.IntegerField()
    mois = models.IntegerField()
    annee = models.IntegerField()
    objects = models.DjongoManager()




class PredictForm(forms.ModelForm):
    
    # def __init__(self,request):
    #     return request
    
    class Meta:
            model = predict
            fields = ('zone', 'typeBien', 'etat', 'nomberEtage', 'surface')
            widgets = {
                'zone': forms.Select(attrs={'class': 'form-control bodytexte'}),
                'typeBien': forms.Select(attrs={'class': 'form-control bodytexte'}),
                'etat': forms.Select(attrs={'class': 'form-control bodytexte'}),
                'nomberEtage': forms.NumberInput(attrs={'class': 'form-control bodytexte','placeholder': u'Nb etage + red chausser','min':1,'max': 30}),
                'surface': forms.NumberInput(attrs={'class': 'form-control bodytexte', 'placeholder': u'surface de logement'}),
            }



