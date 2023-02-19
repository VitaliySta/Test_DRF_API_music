from django.contrib import admin

from .models import (
    Album,
    AlbumSong,
    Performer,
    Song,
)

admin.site.empty_value_display = 'Значение отсутствует'


@admin.register(Performer)
class PerformerAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'title'
    )


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'performer',
        'year'
    )


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'title',
        'get_album_numbers'
    )

    def get_album_numbers(self, obj):
        return [
            f'{album_number.album} - {album_number.number}'
            for album_number in obj.album_numbers.all()
        ]

    get_album_numbers.short_description = 'Исполнитель - год - номер в альбоме'


@admin.register(AlbumSong)
class AlbumSongAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'album',
        'number'
    )
