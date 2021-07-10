
# Create your models here.
from djongo import models
from django.conf import settings
# from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='userprofile')
    description = models.TextField(default="...")
    photo = models.ImageField(upload_to='users',default='user.svg')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('description', 'photo')
        widgets = {
            'description' : forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'file'}),
        }