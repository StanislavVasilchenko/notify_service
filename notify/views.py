from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import generics

from notify.models import Notification
from notify.serializers import NotificationSerializer


@extend_schema(
    request=NotificationSerializer,
    responses={201: NotificationSerializer},
    summary="Sending notifications",
    description="""
    Parameters:
    - message: string up to 1024 characters
    - recipient: string (up to 150 characters) OR list of strings (each up to 150 characters)
    - delay: integer
    """,
)
class NotificationCreate(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
