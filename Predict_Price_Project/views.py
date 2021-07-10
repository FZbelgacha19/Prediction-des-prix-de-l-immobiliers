from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import views
def index(request):
    if (request.user.is_authenticated):
        return redirect('home')
    return render(request, 'index.html')

@login_required
def home(request):
    request.session['field'] = " "
    request.session['filter-value'] = " "
    return HttpResponse(render(request, 'home.html'))