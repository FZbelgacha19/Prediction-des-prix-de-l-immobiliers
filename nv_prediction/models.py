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
    surface_pc = models.IntegerField(verbose_name="Surface couvert",null=False)
    surface_pt = models.IntegerField(verbose_name="Surface terre",null=False)
    avec_toit = models.CharField(verbose_name="Vente Toit",choices=(('oui','oui'),('non','non')),null=False)

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
    class Meta:
            model = predict
            fields = ['zone', 'typeBien', 'etat', 'nomberEtage', 'surface','surface_pc','surface_pt','avec_toit']
            widgets = {
                'zone': forms.Select(attrs={'class': 'form-control'}),
                'typeBien': forms.Select(attrs={'class': 'form-control'}),
                'etat': forms.Select(attrs={'class': 'form-control'}),
                'nomberEtage': forms.NumberInput(attrs={'class': 'form-control','placeholder': u'Nb etage + red chausser','min':1,'max': 30}),
                'surface': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': u'surface de logement','id':'surface'}),
                'surface_pc': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': u'surface couvert','id':'surface_pc'}),
                'surface_pt': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': u'surface de terre reset','readonly': True,'id':'surface_pt'}),
                'avec_toit':forms.Select(attrs={'class': 'form-control'})
            
            }



