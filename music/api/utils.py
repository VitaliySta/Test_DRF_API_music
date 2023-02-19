from rest_framework.validators import ValidationError


def check_uniq(album_song_num, performer, year, number):
    if number in album_song_num:
        raise ValidationError(
            f'В альбоме {performer} {year} песня с №{number} - уже существует!'
        )
