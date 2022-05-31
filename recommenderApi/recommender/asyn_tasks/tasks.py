from time import sleep
from celery import task, shared_task

@shared_task
def send_emails():
    print(f'Sending emails... to 1')
    sleep(10)
    print('Emails sent')
    print('end async task')
    return

@task
def send_schedualed_emails():
    pass