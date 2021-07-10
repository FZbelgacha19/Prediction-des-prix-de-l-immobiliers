import random
from seaborn import color_palette
from operator import itemgetter
from itertools import groupby
import re
from pymongo import MongoClient


def dbPridectionPrix():
    client = MongoClient('localhost:27017')
    return client.Predict_Price_V1


def getPredictionData(user_id):
    db = dbPridectionPrix()
    coll = db.nv_prediction_prediction
    return list(coll.find({"$query" : {"user_id": user_id}, "$orderby": { "annee": -1 } }))


def filterBylist(user_id):
    listdata = getPredictionData(user_id)
    dic = {"":""}
    if(listdata):
        l = list(listdata[0].keys())+['predict.' + str for str in list(listdata[0]['predict'].keys())]
        l = l[3:]
        dic = {str: re.sub(r"(\w)([A-Z])", r"\1 \2",
                        str).replace('predict.', '') for str in l}
    
    return dic


def searchby(field, value, user_id):
    db = dbPridectionPrix()
    coll = db.nv_prediction_prediction
    
    if value.isdigit():
        intval = int(value) if value.isdigit() else -1
        if field == 'price':
            query = {field: {"$gte": intval}}
        else:
            query = {field: intval}
    else:
        val = ".*"+str(value)+".*"
        query = {field: {"$regex": val}}

    query['user_id'] = user_id
    data = list(coll.find(query))
    return data









