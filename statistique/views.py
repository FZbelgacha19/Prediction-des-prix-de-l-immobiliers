from django.shortcuts import render
from .querys import *

from django.contrib.auth.decorators import login_required


@login_required
def statistique_view(request):
    LineLabels,LineDatasets = LineChartData()
    PieData_1,PieData_2 = PieChartData()

    context = {
        'LineLabels':LineLabels,
        'LineDatasets':LineDatasets,
        'PieData_1':PieData_1,
        'PieData_2':PieData_2
        }
    return render(request, 'statistique/statistique.html',context)
    


