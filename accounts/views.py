from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from .models import UserCreateForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'