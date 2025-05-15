from celery import shared_task
from notify.models import Notification, Recipient
from django.core.mail import send_mail

from notify_service import settings


@shared_task
def sent_notify(
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
