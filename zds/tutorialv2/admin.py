from django.contrib import admin

from zds.tutorialv2.models.database import (
    ContentContributionRole,
    ContentReaction,
    ContentRead,
    ContentSuggestion,
    PickListOperation,
    PublicationEvent,
    PublishableContent,
    PublishedContent,
    Validation,
)
from zds.tutorialv2.models.events import Event
from zds.tutorialv2.models.goals import Goal
from zds.tutorialv2.models.help_requests import HelpWriting
from zds.tutorialv2.models.labels import Label


@admin.register(PublishableContent)
class PublishableContentAdmin(admin.ModelAdmin):
    list_display = ("type", "title", "creation_date", "update_date", "is_obsolete")
    list_filter = ("type", "licence", "is_locked", "js_support", "is_obsolete")
    ordering = ("-update_date", "-creation_date")
    raw_id_fields = ("authors", "tags", "image", "gallery", "beta_topic", "last_note", "public_version")
    search_fields = (
        "title",
        "description",
        "source",
        "sha_public",
        "sha_beta",
        "sha_validation",
        "sha_draft",
        "sha_picked",
    )


@admin.register(PublishedContent)
class PublishedContentAdmin(admin.ModelAdmin):
    list_display = ("content", "content_type", "publication_date", "update_date")
    list_filter = (
        "content_type",
        "content__licence",
        "content__is_locked",
        "content__js_support",
        "content__is_obsolete",
    )
    ordering = ("-update_date", "-publication_date")
    raw_id_fields = ("content", "authors")
    search_fields = (
        "content__title",
        "content__description",
        "content__source",
        "content__sha_public",
        "content__sha_beta",
        "content__sha_validation",
        "content__sha_draft",
        "content__sha_picked",
    )


@admin.register(ContentReaction)
class ContentReactionAdmin(admin.ModelAdmin):
    list_display = ("related_content", "author", "ip_address", "pubdate", "is_visible")
    list_filter = ("related_content__type", "is_visible")
    ordering = ("-pubdate",)
    raw_id_fields = ("author", "editor")
    search_fields = ("author__username", "text", "text_hidden", "ip_address")


@admin.register(Validation)
class ValidationAdmin(admin.ModelAdmin):
    list_display = ("content", "date_proposition", "validator", "status")
    list_filter = (
        "status",
        "content__type",
        "content__licence",
        "content__is_locked",
        "content__js_support",
        "content__is_obsolete",
    )
    ordering = ("-date_validation", "-date_reserve", "-date_proposition")
    raw_id_fields = ("content", "validator")
    search_fields = (
        "content__title",
        "content__description",
        "content__source",
        "content__sha_public",
        "content__sha_beta",
        "content__sha_validation",
        "content__sha_draft",
        "content__sha_picked",
    )


@admin.register(PickListOperation)
class PickListOperationAdmin(admin.ModelAdmin):
    list_display = ("content", "operation", "staff_user", "operation_date", "is_effective")
    list_filter = ("is_effective",)
    ordering = ("-operation_date",)
    raw_id_fields = ("content", "staff_user", "canceler_user")
    search_fields = ("content__title", "version")


@admin.register(ContentRead)
class ContentReadAdmin(admin.ModelAdmin):
    list_display = ("content", "user")
    raw_id_fields = ("content", "note", "user")
    search_fields = ("content__title", "user__username")


@admin.register(PublicationEvent)
class PublicationEventAdmin(admin.ModelAdmin):
    list_display = ("published_object", "date", "state_of_processing", "format_requested")
    ordering = ("published_object", "date", "state_of_processing")
    search_fields = ("state_of_processing", "published_object__title", "date")


@admin.register(ContentContributionRole)
class ContentReviewTypeAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]
    ordering = ["position"]


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    ordering = ["position"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    ordering = ["name"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(HelpWriting)
admin.site.register(Event)
admin.site.register(ContentSuggestion)
