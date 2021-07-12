from pymongo import MongoClient,ASCENDING

def dbPridectionPrix():
    client = MongoClient('localhost:27017')
    return client.Predict_Price_V1

def getZoneList():
    db = dbPridectionPrix()
    zn = db.Zone
    # listZone = list(zn.find({},{"_id":0, "zone_name":1, "zone_key":1}).sort([("zone_abr",1)]))
    listZone = list(zn.find({},{"_id":0,"zone_abr":0}).sort([("zone_abr",1)]))
    ZoneTuple = ()
    for dict in listZone:
        values = ()
        for key, value in dict.items():
            values += (str(value),) 
        ZoneTuple +=(values[::-1],)
    # print(ZoneTuple)
    return ZoneTuple

def getTypeBien():
    db = dbPridectionPrix()
    type = db.type_bien
    listType = list(type.find({},{"_id":0,"type_abr":0}))
    TypeTuple = ()
    for dict in listType:
        values = ()
        for key, value in dict.items():
            values += (str(value),)
        TypeTuple +=(values,)
    return TypeTuple


def getEtat():
    db = dbPridectionPrix()
    etats = db.etats
    listEtat= list(etats.find({},{"_id":0,"etat_abr":0}))
    EtatTuple = ()
    for dict in listEtat:
        values = ()
        for key, value in dict.items():
            values += (str(value),)
        EtatTuple +=(values,)
    return EtatTuple

def getdistricts():
    db = dbPridectionPrix()
    data = db.districts
    getData = list(data.find())
    return getData

def finddistricts(value):
    db = dbPridectionPrix()
    data = db.districts
    val= ".*"+str(value)+".*"
    getData = list(data.find({
        "$or": [
            {"zone" : {"$regex" : val, "$options":"$i"}},
            {"code_zone" : {"$regex" :  val.upper(), "$options":"$i"}},
            {"quartiers" : {"$regex" :  val, "$options":"$i"}},
            {"quartiers" : {"$regex" :  val.upper(), "$options":"$i"}},
        ]
        }))
    return getData

def find(name, field,value=""):
    db = dbPridectionPrix()
    print(name, field,value)
    coll = db[name]
    res = coll.find_one({field:value})
    return res

