from django.core.paginator import Paginator
from django.shortcuts import render
# from .forms import predictForm
from .models import PredictForm, Prediction
from .algorithm import predire
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
        # data = [zone,typeBien,etat,nomberEtage]
        price = predire(zone, etat, typeBien, nomberEtage)
        price = surface*price*nomberEtage
        resutat = "Le prix attendu est : "+str(price)+" DH."
        # insertPrediction(zone,etat,typeBien,nomberEtage,surface,price)
        today = date.today()

        p.user = request.user
        Pred_data = {
            'zone': find("Zone", "zone_key", zone)["zone_name"],
            'etat': find("etats", "etat_key", etat)["etat_name"],
            'typeBien': find("type_bien", "type_key", typeBien)["type_name"],
            'nomberEtage': nomberEtage,
            'surface': surface
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


def district_view(request):

    if request.method == "POST":
        value = request.POST['search']
        District_data = finddistricts(value)
    else:
        District_data = getdistricts()

    return render(request, 'nv_prediction/district.html', {'District_data': District_data})
