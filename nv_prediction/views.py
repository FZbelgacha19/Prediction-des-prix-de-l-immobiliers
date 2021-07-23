from typing import List
from django.core.paginator import Paginator
from django.shortcuts import render
# from .forms import predictForm
from .models import PredictForm, Prediction
from .algorithm import get_price, get_Models
from .querys import getdistricts, finddistricts, find
from datetime import date, datetime


from django.contrib.auth.decorators import login_required


@login_required
def main_view(request):
    p = Prediction()
    form = PredictForm(request.POST or None, instance=p)

    if request.method == "POST":
        zone = int(request.POST['zone'])
        etat = int(request.POST['etat'])
        typeBien = int(request.POST['typeBien'])
        nomberEtage = int(request.POST['nomberEtage'])
        surface = int(request.POST['surface'])
        surface_pc = int(request.POST['surface_pc'])
        surface_pt = int(request.POST['surface_pt'])
        avec_toit = request.POST['avec_toit']
# [90, 6, 1, 2, 600, 450, 150, 4150000]
        donnees= [zone,typeBien,etat,nomberEtage,surface,surface_pc,surface_pt]
        svc_pc, svc_pt, rdf_pc, rdf_pt = get_Models()
        price = get_price(donnees,avec_toit,svc_pc, svc_pt, rdf_pc, rdf_pt)

        resutat = "Le prix attendu est : "+str(price)+" DH."
        print(find("Zone", "zone_key", zone))

        today = date.today()
        p.user = request.user
        Pred_data = {
            'zone': find("Zone", "zone_key", zone)["zone_name"],
            'etat': find("etats", "etat_key", etat)["etat_name"],
            'typeBien': find("type_bien", "type_key", typeBien)["type_name"],
            'nomberEtage': nomberEtage,
            'surface': surface,
            'surface_pc': surface_pc,
            'surface_pt': surface_pt,
            'avec_toit':avec_toit
        }
        p.predict = Pred_data
        p.price = price
        p.mois = today.strftime("%m")
        p.annee = today.strftime("%Y")
        p.save()

        # insertPrediction(zone,etat,typeBien,nomberEtage,surface,price)
        
        context = {'form': form, 'resultat': resutat}
        return render(request, 'nv_prediction/NvPrediction.html', context)
    request.session['value'] = " "
    return render(request, 'nv_prediction/NvPrediction.html', {'form': form})

@login_required
def district_view(request):

    if request.method == "POST":
        value = request.POST['search']
        District_data = finddistricts(value)
    else:
        District_data = getdistricts()

    return render(request, 'nv_prediction/district.html', {'District_data': District_data})
