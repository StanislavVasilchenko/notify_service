from notify.models import Notification
from notify.tasks import sent_notify


def sent_notify_for_email_or_tg(
    notification: Notification,
):
    match notification.delay:
        case 0:
            sent_notify.delay(notification.id)
        case 1:
            sent_notify.apply_async(
                args=[notification.id],
                countdown=(notification.scheduled_time - notification.created_at).total_seconds()
            )
        case 2:
            sent_notify.apply_async(
                args=[notification.id],
                countdown=(notification.scheduled_time - notification.created_at).total_seconds()
            )
