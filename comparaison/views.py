from django.shortcuts import render
from .querys import get_test_data
# Create your views here.

def comparaison_view(request):
    data = get_test_data()
    # print(data)

    context = {"data":data}
    return render(request, "comparaison/comparaison.html", context)