from django.shortcuts import render
from .querys import *

from django.contrib.auth.decorators import login_required


@login_required
def immeubles_view(request):
    user_id = request.user.id
    select = filterBylist(user_id)
    DataList = getPredictionData(user_id)

    if request.method == "POST":
        field = request.POST['filtrerPar']
        value = request.POST['search']
        DataList = searchby(field, value, user_id)

    context = {
        'DataList':DataList,
        'select':select,
        }
    return render(request, 'immeubles/immeubles.html',context)
    


