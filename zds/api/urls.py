from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="",
        default_version="",
        description="",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="docs"),
    path("contenus/", include(("zds.tutorialv2.api.urls", "zds.tutorialv2.api"), namespace="content")),
    path("forums/", include(("zds.forum.api.urls", "zds.forum.api"), namespace="forum")),
    path("galeries/", include(("zds.gallery.api.urls", "zds.gallery.api"), namespace="gallery")),
    path("membres/", include(("zds.member.api.urls", "zds.member.api"), namespace="member")),
    path("mps/", include(("zds.mp.api.urls", "zds.mp.api"), namespace="mp")),
    path("", include(("zds.utils.api.urls", "zds.utils.api"), namespace="utils")),
    path("notifications/", include(("zds.notification.api.urls", "zds.notification.api"), namespace="notification")),
]
