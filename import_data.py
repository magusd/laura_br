import csv
import os
from pymongo import MongoClient, IndexModel, ASCENDING, DESCENDING
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(
    os.environ['MONGODB_HOST_SCRIPT'],
    int(os.environ['MONGODB_PORT']))

database = os.environ['MONGODB_DATABASE']
collection = os.environ['MONGODB_COLLECTION']

db = client[database]

#wipe database
db.drop_collection(collection)

#indexes
index1 = IndexModel([("modalidade", ASCENDING), ("data_inicio", DESCENDING)], name="modalidade_inicio")
# index2 = IndexModel([("goodbye", DESCENDING)])
db[collection].create_indexes([index1])

#buffer read csv
data_file = "resources/dataset_estudantes.csv"
with open(data_file) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    batches = 0
    line_count = 0
    bulk_size = 100
    bulk = []
    for row in csv_reader:
        bulk.append(row)
        line_count += 1
        #bulk insert
        if bulk_size <= line_count:
            db[collection].insert_many(bulk)
            batches += 1
            bulk = []
            line_count = 0
    db.students.insert_many(bulk)
    batches += 1
    print(f'Processed {batches} batches.')

