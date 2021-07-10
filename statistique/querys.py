import random
from seaborn import color_palette
from operator import itemgetter
from itertools import groupby
import re
from pymongo import MongoClient


def dbPridectionPrix():
    client = MongoClient('localhost:27017')
    return client.Predict_Price_V1



def getDataForLineChart():
    db = dbPridectionPrix()
    coll = db.nv_prediction_prediction
    query = [
        {
            "$project": {
                "_id": 0,
                "zone": {
                    "$substr": ["$predict.zone", 0, {"$indexOfBytes": ["$predict.zone", "/"]}]
                },
                "price":1,
                "annee":1
            }
        },
        {"$group":
            {
                "_id": {"annee": "$annee", "zone": "$zone"},
                "price": {"$max": "$price"},
                "count": {"$sum": 1}
            }},
        {"$sort": {"_id.annee": 1}}
    ]
    return list(coll.aggregate(query))


def LineChartData():
    Data = getDataForLineChart()
    ChartD = []
    for d in Data:
        x = d['_id']
        y = {'price': d['price']}
        ChartD.append({**x, **y})

    labels = sorted(list(set([d[next(iter(ChartD[1]))] for d in ChartD])))

    chartDtSet = []
    ChartD = sorted(ChartD, key=itemgetter('zone'))
    date = next(iter(ChartD[1]))
    Dark_C = list(color_palette("colorblind", len(ChartD)).as_hex())
    Light_C = list(color_palette("pastel", len(ChartD)).as_hex())
    c = 0
    for key, value in groupby(ChartD, key=itemgetter('zone')):
        tab = [0]*len(labels)
        for d in list(value):
            tab[labels.index(d[date])] = d['price']

        chartDtSet.append({
            "data": tab,
            "label": key,
            "borderColor": Dark_C[c],
            "backgroundColor": Light_C[c],
        })
        c += 1
    return labels, chartDtSet

def getDataForPieChart():
    db = dbPridectionPrix()
    coll = db.nv_prediction_prediction
    query_1 = [
            {
                "$project": {
                    "_id":0,
                    "zone": {
                        "$substr": ["$predict.zone", 0,{"$indexOfBytes": ["$predict.zone", " /"]}]
                    }
            }
            },
            {"$group":
                {
                "_id":{"zone":"$zone"},
                "count":{"$sum":1},
                }},
                {"$sort":{"count":1}}
    ]
    query_2 = [
    {
         "$project":{
             "_id":0,
             "typeBien":"$predict.typeBien",
         }
    },
    {"$group":
        {
        "_id":{"typeBien":"$typeBien"},
        "count":{"$sum":1}
        }},
        {"$sort":{"count":1}}
    ]
    return list(coll.aggregate(query_1)),list(coll.aggregate(query_2))

from json import dumps

def PieChartData():
    Data_1, Data_2 = getDataForPieChart()
    label_1,label_2 = [str(d['_id']['zone']) for d in Data_1],[str(d['_id']['typeBien']) for d in Data_2]
    dataset_1, dataset_2= [d['count'] for d in Data_1],[d['count'] for d in Data_2]
    Dark_C_1,Dark_C_2 = list(color_palette("colorblind", len(label_1)).as_hex()),list(color_palette("colorblind", len(label_2)).as_hex())
    Light_C_1,Light_C_2 = list(color_palette("pastel", len(label_1)).as_hex()),list(color_palette("pastel", len(label_2)).as_hex())
    PieDic_1,PieDic_2 = [{
        "label":label_1,
        "data":dataset_1,
        "borderColor":Dark_C_1,
        "backgroundColor":Light_C_1
    }],[{
        "label":label_2,
        "data":dataset_2,
        "borderColor":Dark_C_2,
        "backgroundColor":Light_C_2
    }]

    return PieDic_1,PieDic_2







