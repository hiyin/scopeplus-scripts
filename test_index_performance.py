from pymongo import MongoClient
import time
import stats
from mongoengine import *

## Connection to DB
#MONGO_HOST = '0.tcp.ap.ngrok.io'
#MONGO_PORT = 11737

class single_cell_meta_country(Document):
   meta_dataset = StringField(max_length=50, db_field="meta_dataset")
   meta_patient_id = IntField(db_field="meta_patient_id")
   meta = {'strict': False}
   
def orm_connector(dbname):
    engine = connect(dbname)
    return engine

     
def db_connector(dbname):

    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017

    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    db = client[dbname]
    return db

## Get cursor
def db_cursor(query):

    pipeline = [
                {"$lookup": { "from": 'matrix', "localField": 'id', "foreignField": 'barcode', "as": 'matrix'} }, 
                {"$match": query  }, 
                {"$project": { "matrix": 1, "_id": 0 } }, 
                {"$unwind": '$matrix' }, 
                {"$replaceRoot": { "newRoot": "$matrix" } }
            ]
    # Test gene table        
    #cursor = db.single_cell_meta_country.aggregate(pipeline)  
    # Test meta table
    cursor =  db.single_cell_meta_country.find(query)  
    return cursor     

def benchmark_index(query):
    """Fetches all documents from the collection page-wise
    """
    #setup(count)
    #print("Start")
    run_count = 3

    times = []

    start_time = time.time()
    for i in range(run_count):
        cursor = db_cursor(query)
    end_time = time.time()
    # Appending time to fetch the page
    times.append((end_time - start_time)/run_count/1000000)

    # returning the time to fetch each page
    return times

def engine_cursor(query_field, query_parameter):
    qset=single_cell_meta_country.objects(query_field=query_parameter).exclude("id")
    return qset

def benchmark_engine(query_field, query_parameter):
    """Fetches all documents from the collection page-wise
    """
    #setup(count)
    #print("Start")
    run_count = 3

    times = []

    start_time = time.time()
    for i in range(run_count):
        cursor = engine_cursor(query_field, query_parameter)
    end_time = time.time()
    # Appending time to fetch the page
    times.append((end_time - start_time)/run_count/1000000)

    # returning the time to fetch each page
    return times

# field_val = db.matrix.distinct("gene_name")
# Matrix table
# for i in field_val:
#     start_time = time.time()
#     #cursor = db['matrix'].find({"gene_name": field_val})
#     cursor = db.single_cell_meta_country.aggregate(pipeline)
#     end_time = time.time()
#     diff = end_time - start_time
#     print(diff)
#     times[i] = diff*1000


def print_stats(times, approach):
    s = stats.all(times)
    print("\"{}\",{},{},{},{}".format(approach, s['mean'], s['p99'], s['p95'], s['p50']))



if __name__ == '__main__':
    print("\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"".format("Approach", "Mean (in seconds)", "p99 (in seconds)", "p95 (in seconds)", "p50 (in seconds)"))

    query = {"meta_dataset": "Ren_2021"}
    dbname = "cov19atlas_new"
    # Test 1 - Index using PyMongo via switching db.matrix.unhideIndex("barcode_1_gene_name_1")
    #db = db_connector(dbname)
    #times = benchmark_index(query)
    #print_stats(times, "no-index")
    #print_stats(times, "with-index")


    # Test 2 - Library 
    # Pymongo
    print("#"+str(query))
    db = db_connector(dbname)
    times = benchmark_index(query)
    print_stats(times, "Pymongo")
    # MongoEngine
    engine = orm_connector(dbname)
    times = benchmark_engine("meta_dataset", "Ren_2021")
    print_stats(times, "MongoEngine")
    # for obj in qset:
    #     print (obj.to_json())   
    # in mongosh 


    # in mongosh db.matrix.hideIndex("barcode_1_gene_name_1")
    
