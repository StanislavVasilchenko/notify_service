import logging

import requests
from celery import shared_task
from django.core.mail import send_mail

from notify.models import DeliveryLog, Notification, Recipient
from notify_service import settings
from notify_service.constant import BASE_URL_TELEGRAM

logger = logging.getLogger(__name__)


@shared_task
def send_notify(
    notification_id: int,
):
    notification = Notification.objects.get(id=notification_id)
    recipients = Recipient.objects.filter(notification=notification)
    for recipient in recipients:
        log_entry = DeliveryLog.objects.get(
            notification=notification,
            recipient=recipient,
            status=DeliveryLog.StatusChoices.PENDING,
        )
        try:
            if not recipient.is_telegram:
                send_mail(
                    subject=notification.message.split(" ")[0],
                    message=notification.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient.address],
                )
            else:
                params = {
                    "chat_id": recipient.address,
                    "text": notification.message,
                }
                requests.post(
                    url=f"{BASE_URL_TELEGRAM}{settings.TG_BOT_TOKEN}/sendMessage",
                    params=params,
                    timeout=10,
                )
            log_entry.status = DeliveryLog.StatusChoices.SUCCESS
            log_entry.save()
        except Exception as e:
            logger.error(f"Failed to send notification: {str(e)}")
            log_entry.status = DeliveryLog.StatusChoices.FAILED
            log_entry.error_message = str(e)
            log_entry.save()
