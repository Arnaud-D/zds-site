from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from zds.tutorialv2.models.database import PublishableContent
from zds.tutorialv2 import signals
from zds.tutorialv2.views.authors import AddAuthorToContent, RemoveAuthorFromContent
from zds.tutorialv2.views.beta import ManageBetaContent
from zds.tutorialv2.views.editorialization import EditContentTags, AddSuggestion, RemoveSuggestion
from zds.tutorialv2.views.help import ChangeHelp
from zds.tutorialv2.views.validations_contents import (
    ReserveValidation,
    AskValidationForContent,
    CancelValidation,
    RejectValidation,
    AcceptValidation,
    RevokeValidation,
    ActivateJSFiddleInContent,
)

# Notes on addition/deletion/update of managed signals
#
# * Addition
#     1. Add a key in signal_to_type.
#     2. Write the corresponding event descriptor function.
#     3. Map the type to the descriptor and voilà !
#
# * Deletion
#     1. Remove the key in signal_to_type and the corresponding @receiver.
#        This will make it impossible to record new events coming from this signal.
#     2. Keep the event descriptor function and the type mapping, so that events in database are displayed properly.
#
# * Update
#     1. If a type name was to be updated for some reason, all the records in the database should also be updated
#        to match this change. Otherwise, no match will be found for the descriptors.


# Map signals to event types
from zds.tutorialv2.views.validations_opinions import PublishOpinion, UnpublishOpinion

types = {
    # Author management
    signals.author_added: "author_added",
    signals.author_removed: "author_removed",
    # Contributor management
    signals.contributor_added: "contributor_added",
    signals.contributor_removed: "contributor_removed",
    # Beta management
    signals.beta_activated: "beta_activated",
    signals.beta_deactivated: "beta_deactivated",
    # Validation management
    signals.validation_requested: "validation_requested",
    signals.validation_canceled: "validation_canceled",
    signals.validation_accepted: "validation_accepted",
    signals.validation_rejected: "validation_rejected",
    signals.validation_revoked: "validation_revoked",
    signals.validation_reserved: "validation_reserved",
    signals.validation_unreserved: "validation_unreserved",
    # Tag management
    signals.tags_modified: "tags_modified",
    # Suggestion managnement
    signals.suggestion_added: "suggestion_added",
    signals.suggestion_removed: "suggestion_removed",
    # Help management
    signals.help_modified: "help_modified",
    # JSFiddle management
    signals.jsfiddle_modified: "jsfiddle_modified",
    # Opinion publication management
    signals.opinion_published: "opinion_published",
    signals.opinion_unpublished: "opinion_unpublished",
}


class Event(models.Model):
    class Meta:
        verbose_name = "Événement sur un contenu"
        verbose_name_plural = "Événements sur un contenu"

    # Base fields
    date = models.DateTimeField(auto_now_add=True)
    performer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=100)
    content = models.ForeignKey(PublishableContent, on_delete=models.CASCADE)

    # Field used by author events
    author = models.ForeignKey(User, related_name="event_author", on_delete=models.SET_NULL, null=True)

    # Field used by contributor events
    contributor = models.ForeignKey(User, related_name="event_contributor", on_delete=models.SET_NULL, null=True)

    # Field used by beta and validation events
    version = models.CharField(null=True, max_length=80)

    @property
    def description(self):
        try:
            return descriptors[self.type.__str__()](self)
        except KeyError:
            return describe_generic(self)


# Event descriptors


def describe_generic(event):
    return _("{} a déclenché un événement inconnu.").format(event.performer)


def describe_author_added(event):
    return _('<a href="{}">{}</a> a ajouté <a href="{}">{}</a> à la liste des auteurs.').format(
        reverse("member-detail", args=[event.performer.username]),
        event.performer,
        reverse("member-detail", args=[event.author.username]),
        event.author,
    )


def describe_author_removed(event):
    return _('<a href="{}">{}</a> a supprimé <a href="{}">{}</a> de la liste des auteurs.').format(
        reverse("member-detail", args=[event.performer.username]),
        event.performer,
        reverse("member-detail", args=[event.author.username]),
        event.author,
    )


def describe_contributor_added(event):
    return _('<a href="{}">{}</a> a ajouté <a href="{}">{}</a> à la liste des contributeurs.').format(
        reverse("member-detail", args=[event.performer.username]),
        event.performer,
        reverse("member-detail", args=[event.contributor.username]),
        event.contributor,
    )


def describe_contributor_removed(event):
    return _('<a href="{}">{}</a> a supprimé <a href="{}">{}</a> de la liste des contributeurs.').format(
        reverse("member-detail", args=[event.performer.username]),
        event.performer,
        reverse("member-detail", args=[event.contributor.username]),
        event.contributor,
    )


def describe_beta_deactivated(event):
    return _('<a href="{}">{}</a> a désactivé la bêta.').format(
        reverse("member-detail", args=[event.performer.username]), event.performer
    )


def describe_beta_activated(event):
    return _('<a href="{}">{}</a> a mis une <a href="{}">version du contenu</a> en bêta.').format(
        reverse("member-detail", args=[event.performer.username]),
        event.performer,
        reverse("content:view", args=[event.content.pk, event.content.slug]) + f"?version={event.version}",
    )


def describe_validation_requested(event):
    return _('<a href="{}">{}</a> a demandé la validation d\'une <a href="{}">version du contenu</a>.').format(
        reverse("member-detail", args=[event.performer.username]),
        event.performer,
        reverse("content:view", args=[event.content.pk, event.content.slug]) + f"?version={event.version}",
    )


def describe_validation_canceled(event):
    return _('<a href="{}">{}</a> a annulé la demande de validation du contenu.').format(
        reverse("member-detail", args=[event.performer.username]), event.performer
    )


def describe_validation_accepted(event):
    return _('<a href="{}">{}</a> a accepté le contenu pour publication.').format(
        reverse("member-detail", args=[event.performer.username]), event.performer
    )


def describe_validation_rejected(event):
    return _('<a href="{}">{}</a> a refusé le contenu pour publication.').format(
        reverse("member-detail", args=[event.performer.username]), event.performer
    )


def describe_validation_revoked(event):
    return _('<a href="{}">{}</a> a dépublié le contenu.').format(
        reverse("member-detail", args=[event.performer.username]), event.performer
    )


def describe_validation_reserved(event):
    return _('<a href="{}">{}</a> a réservé le contenu pour validation.').format(
        reverse("member-detail", args=[event.performer.username]), event.performer
    )


def describe_validation_unreserved(event):
    return _('<a href="{}">{}</a> a annulé la réservation du contenu pour validation.').format(
        reverse("member-detail", args=[event.performer.username]), event.performer
    )


def describe_tags_modified(event):
    return _('<a href="{}">{}</a> a modifié les tags du contenu.').format(
        reverse("member-detail", args=[event.performer.username]), event.performer
    )


def describe_suggestion_added(event):
    return _('<a href="{}">{}</a> a ajouté une suggestion de contenu.').format(
        reverse("member-detail", args=[event.performer.username]), event.performer
    )


def describe_suggestion_removed(event):
    return _('<a href="{}">{}</a> a supprimé une suggestion de contenu.').format(
        reverse("member-detail", args=[event.performer.username]), event.performer
    )


def describe_help_modified(event):
    return _('<a href="{}">{}</a> a modifié les demandes d\'aide.').format(
        reverse("member-detail", args=[event.performer.username]), event.performer
    )


def describe_jsfiddle_modified(event):
    return _('<a href="{}">{}</a> a modifié l\'activation de JSFiddle.').format(
        reverse("member-detail", args=[event.performer.username]), event.performer
    )


def describe_opinion_published(event):
    return _('<a href="{}">{}</a> a publié le billet.').format(
        reverse("member-detail", args=[event.performer.username]), event.performer
    )


def describe_opinion_unpublished(event):
    return _('<a href="{}">{}</a> a dépublié le billet.').format(
        reverse("member-detail", args=[event.performer.username]), event.performer
    )


# Map event types to descriptors
descriptors = {
    "author_added": describe_author_added,
    "author_removed": describe_author_removed,
    "contributor_added": describe_contributor_added,
    "contributor_removed": describe_contributor_removed,
    "beta_activated": describe_beta_activated,
    "beta_deactivated": describe_beta_deactivated,
    "validation_requested": describe_validation_requested,
    "validation_canceled": describe_validation_canceled,
    "validation_accepted": describe_validation_accepted,
    "validation_rejected": describe_validation_rejected,
    "validation_revoked": describe_validation_revoked,
    "validation_reserved": describe_validation_reserved,
    "validation_unreserved": describe_validation_unreserved,
    "tags_modified": describe_tags_modified,
    "suggestion_added": describe_suggestion_added,
    "suggestion_removed": describe_suggestion_removed,
    "help_modified": describe_help_modified,
    "jsfiddle_modified": describe_jsfiddle_modified,
    "opinion_published": describe_opinion_published,
    "opinion_unpublished": describe_opinion_unpublished,
}


# Event recorders


@receiver(signals.beta_activated, sender=ManageBetaContent)
@receiver(signals.beta_deactivated, sender=ManageBetaContent)
def record_event_beta_management(sender, performer, signal, content, version, **_):
    Event(
        performer=performer,
        type=types[signal],
        content=content,
        version=version,
    ).save()


@receiver(signals.author_added, sender=AddAuthorToContent)
@receiver(signals.author_removed, sender=RemoveAuthorFromContent)
def record_event_author_management(sender, performer, signal, content, author, **_):
    Event(
        performer=performer,
        type=types[signal],
        content=content,
        author=author,
    ).save()


@receiver(signals.contributor_added, sender=None)
@receiver(signals.contributor_removed, sender=None)
def record_event_contributor_management(sender, performer, signal, content, contributor, **_):
    Event(
        performer=performer,
        type=types[signal],
        content=content,
        contributor=contributor,
    ).save()


@receiver(signals.validation_requested, sender=AskValidationForContent)
@receiver(signals.validation_canceled, sender=CancelValidation)
@receiver(signals.validation_accepted, sender=AcceptValidation)
@receiver(signals.validation_rejected, sender=RejectValidation)
@receiver(signals.validation_revoked, sender=RevokeValidation)
@receiver(signals.validation_reserved, sender=ReserveValidation)
@receiver(signals.validation_unreserved, sender=ReserveValidation)
def record_event_validation_management(sender, performer, signal, content, version, **_):
    Event(
        performer=performer,
        type=types[signal],
        content=content,
        version=version,
    ).save()


@receiver(signals.tags_modified, sender=EditContentTags)
def record_event_tags_management(sender, performer, signal, content, **_):
    Event(
        performer=performer,
        type=types[signal],
        content=content,
    ).save()


@receiver(signals.suggestion_added, sender=AddSuggestion)
@receiver(signals.suggestion_removed, sender=RemoveSuggestion)
def record_event_suggestion_management(sender, performer, signal, content, **_):
    Event(
        performer=performer,
        type=types[signal],
        content=content,
    ).save()


@receiver(signals.help_modified, sender=ChangeHelp)
def record_event_help_management(sender, performer, signal, content, **_):
    Event(
        performer=performer,
        type=types[signal],
        content=content,
    ).save()


@receiver(signals.jsfiddle_modified, sender=ActivateJSFiddleInContent)
def record_event_jsfiddle_management(sender, performer, signal, content, **_):
    Event(
        performer=performer,
        type=types[signal],
        content=content,
    ).save()


@receiver(signals.opinion_published, sender=PublishOpinion)
@receiver(signals.opinion_unpublished, sender=UnpublishOpinion)
def record_event_opinion_publication_management(sender, performer, signal, content, **_):
    Event(
        performer=performer,
        type=types[signal],
        content=content,
    ).save()
