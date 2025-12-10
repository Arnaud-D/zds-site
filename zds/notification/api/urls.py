from django.urls import path

from zds.notification.api.views import NotificationListAPI

urlpatterns = [
    path("", NotificationListAPI.as_view(), name="list"),
]
