import requests
from celery import shared_task
from notify.models import Notification, Recipient
from django.core.mail import send_mail
from notify_service.constant import BASE_URL_TELEGRAM
from notify_service import settings


@shared_task
def send_notify(
    notification_id: int,
):
    notification = Notification.objects.get(id=notification_id)
    recipients = Recipient.objects.filter(notification=notification)
    for recipient in recipients:
        if not recipient.is_telegram:
            send_mail(
                subject=notification.message.split(" ")[0],
                message=notification.message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient.address]
            )
        else:
            params = {"chat_id": recipient.address, "text": notification.message}
            requests.post(url=f"{BASE_URL_TELEGRAM}{settings.TG_BOT_TOKEN}/sendMessage", params=params)

