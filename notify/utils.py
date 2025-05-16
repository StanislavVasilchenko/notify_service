from typing import List
from notify.models import Notification, DeliveryLog, Recipient
from notify.tasks import send_notify


def sent_notify_for_email_or_tg(
    notification: Notification,
    recipients=List[Recipient],
):
    for recipient in recipients:
        DeliveryLog.objects.create(
            notification=notification,
            recipient=recipient,
            status=DeliveryLog.StatusChoices.PENDING
        )
    send_notify.apply_async(
        args=[notification.id],
        countdown=(notification.scheduled_time - notification.created_at).total_seconds()
    )
