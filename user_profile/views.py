from django.shortcuts import render
from .models import UserProfileForm, UserProfile

from django.contrib.auth.decorators import login_required

@login_required
def index_profile(request):
    UsProfile = UserProfile.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES, instance=UsProfile)
        if form.is_valid():
            up = form.save(commit=False)
            up.user = request.user
            up.save()
    
    form = UserProfileForm(instance=UsProfile)
    return render(request, 'user_profile/index_profile.html',{'form':form,'UsProfile':UsProfile})