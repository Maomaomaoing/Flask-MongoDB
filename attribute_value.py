
def attribute_value():

    from pymongo import MongoClient
    from urllib.parse import quote_plus
    
    """ 連接MongoDB """
    uri = "mongodb://%s:%s@%s" % (quote_plus('Mao'), quote_plus('7711'), quote_plus('127.0.0.1'))
    client = MongoClient(uri)
    cllct = client.admin.homicide  
    del_attr = set(['City', 'Agency Name', '_id', 'Agency Code', 
                    'Incident', 'Record ID', 'Victim Age', 
                    'Perpetrator Age', 'Record Source'])
    attr = set(cllct.find_one({}).keys())
    attr = list(attr-del_attr)
   
    value_list = []   
    for a in attr:
        value_set = set()
        for r in cllct.find():
            value_set.update({r[a]})
        value_list.append(list(value_set))
    
    value_dict = dict(zip(attr, value_list))
    return value_dict