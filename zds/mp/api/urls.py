from django.urls import path, re_path

from zds.mp.api.views import (
    PrivatePostDetailAPI,
    PrivatePostListAPI,
    PrivatePostReactionKarmaView,
    PrivateTopicDetailAPI,
    PrivateTopicListAPI,
    PrivateTopicReadAPI,
)

urlpatterns = [
    path("", PrivateTopicListAPI.as_view(), name="list"),
    re_path(r"^(?P<pk>[0-9]+)/?$", PrivateTopicDetailAPI.as_view(), name="detail"),
    path("<int:pk_ptopic>/messages/", PrivatePostListAPI.as_view(), name="message-list"),
    re_path(
        r"^(?P<pk_ptopic>[0-9]+)/messages/(?P<pk>[0-9]+)/?$", PrivatePostDetailAPI.as_view(), name="message-detail"
    ),
    path(
        "<int:pk_ptopic>/messages/<int:pk>/karma/",
        PrivatePostReactionKarmaView.as_view(),
        name="mp-reaction-karma",
    ),
    path("unread/", PrivateTopicReadAPI.as_view(), name="list-unread"),
]
