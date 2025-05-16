from datetime import timedelta

from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils import timezone


class Delay(models.IntegerChoices):
    IMMEDIATELY = (0, "Send now")
    ONE_HOUR = (1, "Send in an hour")
    ONE_DAY = (2, "Send in a day")


class Notification(models.Model):
    message = models.TextField(
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(1024),
        ],
        verbose_name="Message",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    scheduled_time = models.DateTimeField(verbose_name="Scheduled time")
    delay = models.PositiveSmallIntegerField(
        choices=Delay.choices,
        default=Delay.IMMEDIATELY,
        verbose_name="Delay",
    )

    def __str__(self):
        return f"Notification {self.id}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def save(self, *args, **kwargs):
        now = timezone.now()
        if self.delay == Delay.ONE_HOUR:
            self.scheduled_time = now + timedelta(hours=1)
        elif self.delay == Delay.ONE_DAY:
            self.scheduled_time = now + timedelta(days=1)
        else:
            self.scheduled_time = now
        super().save(*args, **kwargs)
