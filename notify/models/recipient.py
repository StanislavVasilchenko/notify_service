from django.db import models

from notify.models import Notification


class Recipient(models.Model):
    address = models.JSONField(max_length=150, verbose_name="address", default=list)
    is_telegram = models.BooleanField(
        default=False,
        verbose_name="is_telegram",
        blank=True,
        null=True,
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="recipient",
        verbose_name="notification")

    def __str__(self):
        return f"{self.address} ({'telegram' if self.is_telegram else 'email'})"

    class Meta:
        verbose_name = "recipient"
        verbose_name_plural = "recipients"

    def save(self, *args, **kwargs):
        if isinstance(self.address, list):
            for address in self.address:
                if address.isdigit():
                    self.is_telegram = address.isdigit()
        elif isinstance(self.address, str):
            self.is_telegram = self.address.isdigit()
        super().save(*args, **kwargs)
