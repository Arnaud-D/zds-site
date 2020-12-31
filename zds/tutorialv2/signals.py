from django.dispatch.dispatcher import Signal

# Display management
content_read = Signal(providing_args=["instance", "user", "target"])

# Publication events
content_published = Signal(providing_args=["instance", "user", "by_email"])
content_unpublished = Signal(providing_args=["instance", "target", "moderator"])

# Author management
# For the signals below, the arguments "performer", "content" and "author" shall be provided.
author_added = Signal()
author_removed = Signal()

# Contributor management
# For the signals below, the arguments "performer", "content" and "contributor" shall be provided.
contributor_added = Signal()
contributor_removed = Signal()

# Beta management
# For the signals below, the arguments "performer", "content" and "version" shall be provided.
beta_activated = Signal()
beta_deactivated = Signal()

# Validation management
# For the signals below, the arguments "performer", "content" and "version" shall be provided.
validation_requested = Signal()
validation_canceled = Signal()
validation_accepted = Signal()
validation_rejected = Signal()
validation_revoked = Signal()
validation_reserved = Signal()
validation_unreserved = Signal()

# Tags management
# For the signal below, the arguments "performer" and "content"  shall be provided.
tags_modified = Signal()

# Suggestion management
# For the signals below, the arguments "performer" and "content"  shall be provided.
suggestion_added = Signal()
suggestion_removed = Signal()

# Help management
# For the signal below, the arguments "performer" and "content"  shall be provided.
help_modified = Signal()

# JSFiddle management
# For the signal below, the arguments "performer" and "content"  shall be provided.
jsfiddle_modified = Signal()
