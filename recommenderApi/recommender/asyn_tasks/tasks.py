from time import sleep
from celery import task, shared_task
from recommender.collobarative.seenTable import SeenTable

@shared_task
def send_emails():
    print(f'Sending emails... to 1')
    sleep(10)
    print('Emails sent')
    print('end async task')
    return

@shared_task
def addToSeenTable(seenTable: SeenTable, userId, itemIds):
    print('adding to seen table')
    seenTable.addToSeenTable(userId, itemIds)
    return None

# @task
# def send_schedualed_emails():
#     pass