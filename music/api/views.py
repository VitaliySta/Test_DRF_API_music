from rest_framework import status, viewsets
from rest_framework.response import Response

from music_albums.models import (
    Album,
    AlbumSong,
    Performer,
    Song,
)

from .serializers import (
    AlbumSerializer,
    PerformerSerializer,
    SongSerializer,
)


class PerformerViewSet(viewsets.ModelViewSet):
    """API endpoint that allows performers to be viewed or edited."""

    queryset = Performer.objects.all()
    serializer_class = PerformerSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    """API endpoint that allows albums to be viewed or edited."""

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class SongViewSet(viewsets.ModelViewSet):
    """API endpoint that allows songs to be viewed or edited."""

    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def destroy(self, request, *args, **kwargs):
        song = self.get_object()
        album_songs = song.album_numbers.all()
        album_songs.delete()
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
