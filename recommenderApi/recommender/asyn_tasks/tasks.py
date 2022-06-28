from time import sleep
from celery import task, shared_task
from recommender.collobarative.train import train_and_update
from recommender.mongoDB.getData import MongoConnection
from recommender.sqliteDB.data import SQLite_Database
from recommenderApi.imports import MongoClient, certifi, dt, ObjectId, dump, load
from recommenderApi.settings import MONGODB_LINK, MONGODB_NAME, ROUND_NUM_OF_REVIEWS
from recommender.sqliteDB.data import SQLite_Database

# @shared_task
# def send_emails(user = 10):
#     print(f'Sending emails... to {user}')
#     sleep(10)
#     print('Emails sent')
#     print('end async task')
#     return

@shared_task
def start_async(date, first):
    print('start async task')
    print(dt.fromisoformat(date))
    print('check try block')
    try: 
        vars = load(open('recommenderApi/vars.pkl', 'rb'))
        print(f"(try block) time is: {vars['date']}")
    except:
        vars = {}
        print('(except block) vars is empty')

    print('end try block')
    dump(vars, open('recommenderApi/vars.pkl', 'wb'))
    print('dump file')
    # train_and_update(dt.fromisoformat(date), first=first)
    print('end async task')
    return

@shared_task
def start_async2():
    print('start async task')
    # with MongoClient(MONGODB_LINK, tlsCAFile=certifi.where()) as client:
    #     db = client[MONGODB_NAME]
    users = MongoConnection().get_users_mongo(dt(2020, 1,1))
    for user in users:
        print(user)
        break
    print('end async task')
    return

# @task
# def send_schedualed_emails():
#     print('Sending emails... to user...')