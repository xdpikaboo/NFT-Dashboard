from pymongo import MongoClient
from analysis.utils import logging

MONGO_ENDPOINT = 'mongodb+srv://hieunguyen:Hieu1234@hieubase.r9ivh.gcp.mongodb.net'
MONGO_PORT = 27017

DATABASE_NAME = 'nft-dashboard'
ANAL_COLLECTION = 'collection_anal'
DB_COLLECTION = 'dashboarditems'

client = MongoClient(MONGO_ENDPOINT, MONGO_PORT)
# db = client[DATABASE_NAME]


def get_collection(collection_name, db_name=DATABASE_NAME, cloud=False):
    current_client = client
    current_db = current_client[db_name]
    collection = current_db[collection_name]
    return collection

def get_db_rows(tag=None):
    if not tag:
        return list(get_collection(DB_COLLECTION).find())
    else:
        return list(get_collection(DB_COLLECTION).find({'tag': tag}))

def write_metrics(collection_data):
    anal_col = get_collection(ANAL_COLLECTION)
    anal_col.update_one({'symbol': collection_data['symbol']}, {'$set': collection_data}, upsert=True)

def drop_upcoming():
    anal_col = get_collection(ANAL_COLLECTION)
    anal_col.delete_many({'tag': 'upcoming'})

def drop_tag(tag):
    anal_col = get_collection(ANAL_COLLECTION)
    anal_col.delete_many({'tag': tag})

def insert_analysis(cols):
    anal_col = get_collection(ANAL_COLLECTION)
    try: 
      anal_col.insert_many(cols, ordered=False)
    except:
      logging.warn("Duplicates Collection")

def insert_or_update_many_records(cols, collection):
    try:
    #   collection.insert_many(cols, ordered=False)
        for col in cols:
            _id = col['_id']
            collection.replace_one({"_id": _id}, col, upsert=True)
    except:
        logging.warn("Bugs at insert_or_update_many_records in db.py")

def drop_then_insert(cols, tag=None):
    if not tag:
        tag_filter = list(filter(lambda col: 'tag' in col, cols))
        if len(tag_filter) > 0:
            tag = tag_filter[0]['tag']
        else:
            ## No tag was found in the collections. Weird
            return 
            
    drop_tag(tag)
    insert_analysis(cols)

def drop_all_then_insert_many(data, collection_name):
    all_nfts_col = get_collection(collection_name)
    all_nfts_col.delete_many({})
    all_nfts_col.insert_many(data)

def drop_by_tag(tag, collection_name):
    try:
        all_nfts_col = get_collection(collection_name)
        all_nfts_col.delete_many({tag: True})
    except Exception as e:
        logging.warn(e)

def insert_many(data, collection_name):
    try:
        col = get_collection(collection_name)
        col.insert_many(data, ordered=False)
    except Exception as e:
        logging.warn(e)

def query_from_collection(query, collection_name):
    col = get_collection(collection_name)
    res = list(col.find(query))
    return res

def get_distinct(key):
    return get_collection(DB_COLLECTION).distinct(key)