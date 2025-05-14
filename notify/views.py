from rest_framework import generics

from notify.models import Notification
from notify.serializers import NotificationSerializer


class NotificationCreate(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
