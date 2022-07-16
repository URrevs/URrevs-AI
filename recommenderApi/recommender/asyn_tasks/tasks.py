from celery import shared_task
from recommender.mongoDB.getData import MongoConnection
from recommender.collobarative.train import train_and_update
from recommenderApi.imports import dt, requests
from recommenderApi.settings import STOP_TRAINING, API_KEY_SECRET

@shared_task
def start_async(date, first):
    print(dt.fromisoformat(date))
    print('start async task')
    train_and_update(dt.fromisoformat(date), first=first)
    try:
        headersList = {
            "Accept": "*/*",
            "User-Agent": "Thunder Client (https://www.thunderclient.com)",
            'x-api-key': API_KEY_SECRET,
        }
        response = requests.request("GET", STOP_TRAINING, data="",  headers=headersList)
        print('request sent and response: ', response.text)
    except Exception as e: 
        print(e)
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