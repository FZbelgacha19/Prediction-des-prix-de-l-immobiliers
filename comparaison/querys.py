import random
from pymongo import MongoClient
# from predict_price_project.nv_prediction.algorithm import get_price
from nv_prediction.algorithm import get_price

def dbPridectionPrix():
    client = MongoClient('localhost:27017')
    return client.Predict_Price_V1

def get_test_data():
    db = dbPridectionPrix()
    test = db.test
    zone = db.Zone
    etat = db.etats
    typBien = db.type_bien

    test_lst = list(test.find({},{'_id':0}))
    i=2
    for dic in test_lst:
        l = [dic["zone"],dic["type"],dic["etat"],dic["etage"],dic["surface"],dic["Su_Cov"],dic["Su_terr"]]
        dic["prix_pred"] = get_price(l,dic["avec_toit"])
        dic["img_index"] = str(i)+".jpg"
        dic["zone"] = zone.find_one({"zone_key":dic["zone"]})["zone_name"]
        dic["type"] = typBien.find_one({"type_key":dic["type"]})["type_name"]
        dic["etat"] = etat.find_one({"etat_key":dic["etat"]})["etat_name"]
        i+=1
    
    return test_lst