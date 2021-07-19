from pymongo import MongoClient

import pandas as pd
import numpy as np


from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier

def getDataFrame():
    client = MongoClient('localhost:27017')
    db = client.Predict_Price_V1

    #get la collection dataset
    data = db.dataset
    df = pd.DataFrame(list(data.find()))
    return df


def train_x_y(dataframe):
    """train_x_y permet de crée les x, y pour faire trainement

    Args:
        dataframe : dataset
    """
    
    #modification de dataset (suppression de column id)
    dataframe = dataframe.drop('_id', axis=1)

    #deviser les donner sous form target et feautre
    x = dataframe.drop(['PC','PT'], axis=1)
    y_pc = dataframe['PC']
    y_pt = dataframe['PT']
    
    return x, y_pc, y_pt

def predicts(model,zone, Tbien,etat,etage):
    """Permet de prédire le prix de m²

    Args:
        model : model de prediction
        zone : zone de bien
        Tbien : Type de bien
        etat : etat de bien
        etage : nomber des etages R+Nb_Etage

    Returns:
        price
    """
    data = np.array([zone, Tbien,etat,etage],dtype=int).reshape(1,-1)
    pred = model.predict(data)
    price = round(int(pred[0]))
    return price

def calculer_price(surface,price,etage=1):
    """
    calculer prix
    """
    return surface*price*etage

def Average(liste):
    """Permet Calculer le moyen
    """
    return sum(liste) / len(liste)

def getMin(liste, avg):
    """getMin return minimum d'un liste
    """
    LMin = []
    for l in liste:
        LMin.append(abs(l-avg))
    i = LMin.index(min(LMin))
    return liste[i]


def RFClassif(x,y):
    r = RandomForestClassifier(n_estimators=100,random_state=0)
    r.fit(x, y)
    return r


def SVClassif(x,y):
    s = make_pipeline(StandardScaler(), SVC())
    s.fit(x, y)
    return s

def get_Models():
    dataframe = getDataFrame()
    X, Y_pc, Y_pt = train_x_y(dataframe)
    rdf_pc = RFClassif(X,Y_pc)
    rdf_pt = RFClassif(X,Y_pt)

    svc_pc = SVClassif(X,Y_pc)
    svc_pt = SVClassif(X,Y_pt)

    return svc_pc, svc_pt, rdf_pc, rdf_pt

def get_price(L_test,avec_toit,svc_pc, svc_pt, rdf_pc, rdf_pt):

    # [zone-0,typeBien-1,etat-2,nomberEtage-3,surface-4,surface_pc-5,surface_pt-6]
    rdf_pc_pred = predicts(rdf_pc,L_test[0], L_test[1],L_test[2],L_test[3])
    svc_pc_pred = predicts(svc_pc,L_test[0], L_test[1],L_test[2],L_test[3])

    rdf_pt_pred = predicts(rdf_pt,L_test[0], L_test[1],L_test[2],L_test[3])
    svc_pt_pred = predicts(svc_pt,L_test[0], L_test[1],L_test[2],L_test[3])

    toit_price = 0
    if(avec_toit == 'oui'):
        toit_price = min([calculer_price(L_test[5],rdf_pc_pred),calculer_price(L_test[5],svc_pc_pred)])

    lst_pc = [calculer_price(L_test[5],rdf_pc_pred,L_test[3]),calculer_price(L_test[5],svc_pc_pred,L_test[3])]
    lst_pt = [calculer_price(L_test[6],rdf_pt_pred),calculer_price(L_test[6],svc_pt_pred)]

    price = getMin(lst_pc,Average(lst_pc))+getMin(lst_pt,Average(lst_pt))+toit_price
    
    return price
