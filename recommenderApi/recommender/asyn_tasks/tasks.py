from time import sleep
from celery import task, shared_task
from recommender.collobarative.train import train_and_update

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
    train_and_update(date, first=first)
    print('end async task')
    return

# @task
# def send_schedualed_emails():
#     print('Sending emails... to user...')