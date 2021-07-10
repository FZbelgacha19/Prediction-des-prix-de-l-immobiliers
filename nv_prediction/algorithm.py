import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier

#Connection avec base de donner
from pymongo import MongoClient


def predire(zone, etat, Tbien, etage):
    client = MongoClient('localhost:27017')
    db = client.Predict_Price_V1

    #get la collection dataset
    data = db.dataset
    dataframe = pd.DataFrame(list(data.find()))

    #modification de dataset (suppression de column id)
    dataframe = dataframe.drop('_id', axis=1)

    #deviser les donner sous form target et feautre
    X = dataframe.drop('Prix_au_m_carre', axis=1)
    Y = dataframe['Prix_au_m_carre']

   
    #training the model
    model = RandomForestClassifier(n_estimators=200)
    model.fit(X, Y)
    # model.predict(x_test)
    #appliquer la prediction
    data = np.array([zone, Tbien,etat,etage],dtype=int).reshape(1,-1)
    pred = model.predict(data)
    price = round(pred[0])
    return price


