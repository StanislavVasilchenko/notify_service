from django.db import models

from notify.models import Notification, Recipient
from notify_service.constant import NULLABLE


class DeliveryLog(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", "В ожидании"
        SUCCESS = "success", "Успешно"
        FAILED = "failed", "Не удалось"

    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="notification_logs",
        verbose_name="notification",
    )
    recipient = models.ForeignKey(
        Recipient,
        on_delete=models.CASCADE,
        related_name="recipient_logs",
        verbose_name="recipient",
    )
    status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.SUCCESS,
        max_length=10,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created")
    error_message = models.TextField(verbose_name="error", **NULLABLE)

    class Meta:
        verbose_name = "delivery_log"
        verbose_name_plural = "delivery_logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"LOG {self.id} - {self.status}"
