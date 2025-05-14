from rest_framework import serializers

from notify.models import Notification, Recipient


class RecipientField(serializers.Field):

    def to_internal_value(self, data):

        if isinstance(data, str):
            return [data]
        elif isinstance(data, list):
            if all(isinstance(item, str) for item in data):
                return data
            raise serializers.ValidationError("Все элементы должны быть строками.")
        else:
            raise serializers.ValidationError("recipient должен быть строкой или списком строк.")

    def to_representation(self, value):
        return [recipient.address for recipient in value.all()]


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

        [Recipient.objects.create(
            address=address,
            notification=notification,
        ) for address in validated_data.get("recipient")]

        return notification
