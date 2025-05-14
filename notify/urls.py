from django.urls import path
from notify.views import NotificationCreate

app_name = "notify"

urlpatterns = [
    path("notify/", NotificationCreate.as_view(), name="notify"),
]
