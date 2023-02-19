from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import SimpleRouter

from .views import (
    AlbumViewSet,
    PerformerViewSet,
    SongViewSet,
)

router = SimpleRouter()
router.register('performers', PerformerViewSet)
router.register('albums', AlbumViewSet)
router.register('songs', SongViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Music API",
        default_version='v1',
        description="Документация для приложения Music",
    ),
    public=True,
)


urlpatterns = [
    path('', include(router.urls)),
    path(
        'docs/', schema_view.with_ui('swagger', cache_timeout=0),
        name='swagger'
    ),
]
