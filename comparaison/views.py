from django.shortcuts import render
from .querys import get_test_data, getScatterData
# Create your views here.

from django.contrib.auth.decorators import login_required


@login_required
def Donnees_view(request):
    data = get_test_data()
    # print(data)

    context = {"data":data}
    return render(request, "comparaison/Donnees.html", context)

@login_required
def Graph_view(request):
    data = get_test_data()
    ScatterLabels, ScatterDatasets = getScatterData(data)
    context = {"ScatterLabels":ScatterLabels, "ScatterDatasets":ScatterDatasets}
    # context = {}
    return render(request, "comparaison/Graph.html", context)