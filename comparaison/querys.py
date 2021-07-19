import random
from pymongo import MongoClient
# from predict_price_project.nv_prediction.algorithm import get_price
from nv_prediction.algorithm import get_price, get_Models

def dbPridectionPrix():
    client = MongoClient('localhost:27017')
    return client.Predict_Price_V1

def get_test_data():
    db = dbPridectionPrix()
    test = db.test
    zone = db.Zone
    etat = db.etats
    typBien = db.type_bien
    svc_pc, svc_pt, rdf_pc, rdf_pt = get_Models()
    test_lst = list(test.find({},{'_id':0}))
    i=2
    for dic in test_lst:
        l = [dic["zone"],dic["type"],dic["etat"],dic["etage"],dic["surface"],dic["Su_Cov"],dic["Su_terr"]]
        dic["prix_pred"] = get_price(l,dic["avec_toit"],svc_pc, svc_pt, rdf_pc, rdf_pt)
        dic["img_index"] = str(i)+".jpg"
        dic["zone"] = zone.find_one({"zone_key":dic["zone"]})["zone_name"]
        dic["type"] = typBien.find_one({"type_key":dic["type"]})["type_name"]
        dic["etat"] = etat.find_one({"etat_key":dic["etat"]})["etat_name"]
        i+=1
    
    return test_lst

def getScatterData(test_lst):
    # labels = ["Bien n° "+str(i) for i in range(1, len(test_lst)+1)]
    labels = [i for i in range(1, len(test_lst)+1)]
    index = 1
    prix_reel = []
    prix_pred = []
    chartDtSet = []
    for l in test_lst:
        prix_reel.append({
            "x":index,
            "y":l["prix_reel"]
        })
        prix_pred.append({
            "x":index,
            "y":l["prix_pred"]
        })
        index+=1


    chartDtSet.append({
        "data" : prix_reel,
        "label" : "Prix réel",
        "borderColor": "#9DAAF2",
        "backgroundColor":"#9DAAF2"
    })
    chartDtSet.append({
        "data" : prix_pred,
        "label" : "Prix predicte",
        "borderColor": "#FF6A3D",
        "backgroundColor":"#FF6A3D"
    })

    return labels, chartDtSet