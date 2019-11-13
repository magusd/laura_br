import csv
dataset = "resources/dataset_estudantes.csv"
with open(dataset) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    bulk_size = 100
    x = 0
    bulk = []
    for row in csv_reader:
        bulk.append(row)
        line_count+=1
        if(bulk_size <= line_count):
            x+=1
            print(x)
            bulk=[]
            line_count=0
    print(f'Processed {line_count} lines.')

# from dotenv import load_dotenv
# load_dotenv()
# client = MongoClient(
#     os.environ['MONGODB_HOST_SCRIPT'],
#     os.environ['MONGODB_PORT'])
# db = client.students
