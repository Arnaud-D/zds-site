from django.conf import settings
from django.contrib import admin

from .models import PrivatePost, PrivateTopic, PrivateTopicRead

if settings.DEBUG:

    @admin.register(PrivatePost)
    class PrivatePostAdmin(admin.ModelAdmin):
        """Representation of PrivatePost model in the admin interface."""

        list_display = ("privatetopic", "author", "pubdate", "update", "position_in_topic")
        raw_id_fields = ("privatetopic", "author")

    @admin.register(PrivateTopic)
    class PrivateTopicAdmin(admin.ModelAdmin):
        """Representation of PrivateTopic model in the admin interface."""

        list_display = ("title", "subtitle", "author", "last_message", "pubdate")
        raw_id_fields = ("author", "participants", "last_message")

    @admin.register(PrivateTopicRead)
    class PrivateTopicReadAdmin(admin.ModelAdmin):
        """Representation of PrivateTopicRead model in the admin interface."""

        list_display = ("privatetopic", "privatepost", "user")
        raw_id_fields = ("privatetopic", "privatepost", "user")
