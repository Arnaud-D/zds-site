from django.contrib import admin

from zds.member.models import (
    Ban,
    BannedEmailProvider,
    BlockedIP,
    KarmaNote,
    NewEmailProvider,
    Profile,
    TokenForgotPassword,
    TokenRegister,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Representation of Profile model in the admin interface."""

    list_display = ("user", "last_ip_address", "can_read", "end_ban_read", "can_write", "end_ban_write", "last_visit")
    list_filter = ("can_read", "can_write")
    ordering = ("-last_visit",)
    raw_id_fields = ("user",)
    search_fields = ("user__username", "sign", "site", "avatar_url", "biography", "last_ip_address")


@admin.register(Ban)
class BanAdmin(admin.ModelAdmin):
    """Representation of Ban model in the admin interface."""

    list_display = ("user", "moderator", "type", "note", "pubdate")
    list_filter = ("type",)
    ordering = ("-pubdate",)
    raw_id_fields = ("user", "moderator")
    search_fields = ("user__username", "note")


@admin.register(TokenRegister)
class TokenRegisterAdmin(admin.ModelAdmin):
    """Representation of TokenRegister model in the admin interface."""

    list_display = ("user", "date_end")
    search_fields = ("user__username",)
    raw_id_fields = ("user",)


@admin.register(TokenForgotPassword)
class TokenForgotPasswordAdmin(admin.ModelAdmin):
    """Representation of TokenForgotPassword model in the admin interface."""

    list_display = ("user", "date_end")
    search_fields = ("user__username",)
    raw_id_fields = ("user",)


@admin.register(KarmaNote)
class KarmaNoteAdmin(admin.ModelAdmin):
    """Representation of KarmaNote model in the admin interface."""

    list_display = ("user", "moderator", "note", "karma", "pubdate")
    ordering = ("-pubdate",)
    search_fields = ("user__username", "note")
    raw_id_fields = ("user", "moderator")


@admin.register(NewEmailProvider)
class NewEmailProviderAdmin(admin.ModelAdmin):
    """Representation of NewEmailProvider model in the admin interface."""

    list_display = ("provider", "user", "date")
    list_filter = ("use",)
    ordering = ("-date",)
    search_fields = ("provider", "user__username")
    raw_id_fields = ("user",)


@admin.register(BannedEmailProvider)
class BannedEmailProviderAdmin(admin.ModelAdmin):
    """Representation of BannedEmailProvider model in the admin interface."""

    list_display = ("provider", "moderator", "date")
    ordering = ("-date",)
    search_fields = ("provider",)
    raw_id_fields = ("moderator",)


@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    """Representation of BlockedIP model in the admin interface"""

    list_display = ("ip_address", "is_network_address", "moderator", "reason")
    ordering = ("-blocked_date",)
    search_fields = ("ip_address", "moderator")
    raw_id_fields = ("moderator",)
