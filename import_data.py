import csv
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(
    os.environ['MONGODB_HOST_SCRIPT'],
    int(os.environ['MONGODB_PORT']))
db = client.laura_br

data_file = "resources/dataset_estudantes.csv"
with open(data_file) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    bulk_size = 100
    bulk = []
    for row in csv_reader:
        bulk.append(row)
        line_count += 1
        if bulk_size <= line_count:
            db.students.insert_many(bulk)
            bulk = []
            line_count = 0
    print(f'Processed {line_count} lines.')

