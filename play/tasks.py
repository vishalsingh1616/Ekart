from time import sleep
from celery import shared_task # type: ignore

@shared_task
def notify_user(message):
    print("Sending notification to user...")
    print(message)
    sleep(5)
    print("Notification sent.")
