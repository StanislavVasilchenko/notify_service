from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from notify.models import Notification, Recipient
from notify.utils import sent_notify_for_email_or_tg


class RecipientField(serializers.Field):

    def to_internal_value(self, data):

        if isinstance(data, str):
            return [data]
        elif isinstance(data, list):
            if all(isinstance(item, str) for item in data):
                return data
            raise serializers.ValidationError("Все элементы должны быть строками.")
        else:
            raise serializers.ValidationError(
                "recipient должен быть строкой или списком строк.",
            )

    def to_representation(self, value):
        return [recipient.address for recipient in value.all()]


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "One recipient",
            value={
                "message": "Message text",
                "recipient": "email@example.com",
                "delay": 0,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Many recipients",
            value={
                "message": "Message text",
                "recipient": ["email1@example.com", "email2@example.com", "123456789"],
                "delay": 0,
            },
            request_only=True,
        ),
    ],
)
class NotificationSerializer(serializers.ModelSerializer):
    recipient = RecipientField(write_only=True)

    class Meta:
        model = Notification
        fields = ["message", "recipient", "delay"]

    def create(self, validated_data):
        notification = Notification.objects.create(
            message=validated_data.get("message"),
            delay=validated_data.get("delay"),
        )

        recipients = [
            Recipient(
                address=adr,
                notification=notification,
                is_telegram=True if adr.isdigit() else False,
            )
            for adr in validated_data.get("recipient")
        ]

        Recipient.objects.bulk_create(recipients)

        sent_notify_for_email_or_tg(
            notification=notification,
            recipients=recipients,
        )

        return notification
