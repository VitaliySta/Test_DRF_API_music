from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from music_albums.models import (
    Album,
    AlbumSong,
    Performer,
    Song,
)

from .utils import check_uniq


class PerformerSerializer(serializers.ModelSerializer):
    """Serializer for Performer model."""

    class Meta:
        model = Performer
        fields = (
            'pk',
            'title'
        )


class AlbumSerializer(serializers.ModelSerializer):
    """Serializer for Album model."""

    class Meta:
        model = Album
        fields = ('pk', 'performer', 'year')
        validators = [
            UniqueTogetherValidator(
                queryset=Album.objects.all(),
                fields=('performer', 'year'),
                message='Введенные performer и year уже существует!!!'
            )
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['performer'] = instance.performer.title
        return ret


class AlbumSongSerializer(serializers.ModelSerializer):
    """Serializer for AlbumSong model."""

    class Meta:
        model = AlbumSong
        fields = ('album', 'number')


class SongSerializer(serializers.ModelSerializer):
    """Serializer for Song model."""

    album_numbers = AlbumSongSerializer(many=True)

    class Meta:
        model = Song
        fields = ('pk', 'title', 'album_numbers')

    def validate(self, data):
        for album_number in data['album_numbers']:
            performer = album_number['album'].performer
            year = album_number['album'].year
            number = album_number['number']
            album = Album.objects.get(performer=performer, year=year).pk
            album_song_num = [
                i.number for i in AlbumSong.objects.filter(album=album)
            ]
            flag = album_number['album'] != data['album_numbers'][-1]['album']
            if self.context.get('request').method == 'POST':
                check_uniq(album_song_num, performer, year, number)
                if flag:
                    continue
                return data
            if self.context.get('request').method in ['PUT', 'PATCH']:
                obj_pk = self.instance.pk
                current_obj = {
                    i.album: i.number for i in
                    Song.objects.get(pk=obj_pk).album_numbers.all()
                }
                try:
                    if current_obj[album_number['album']] == album_number[
                        'number'
                    ]:
                        if flag:
                            continue
                        return data
                    else:
                        check_uniq(album_song_num, performer, year, number)
                except KeyError:
                    check_uniq(album_song_num, performer, year, number)
                    if flag:
                        continue
                    return data
            return data

    def create(self, validated_data):
        album_numbers = validated_data.pop('album_numbers')
        song = Song.objects.create(**validated_data)
        for album_number in album_numbers:
            current_album = Album.objects.get(
                pk=album_number['album'].pk
            )
            number = AlbumSong.objects.create(
                album=current_album,
                number=album_number['number']
            )
            song.album_numbers.add(number)
        return song

    def update(self, instance, validated_data):
        album_numbers = validated_data.pop('album_numbers')
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        existing_numbers = instance.album_numbers.all()
        existing_numbers_dict = {
            f"{an.album_id}": an for an in existing_numbers
        }
        updated_numbers = []
        for album_number in album_numbers:
            album_id = album_number['album'].pk
            number = album_number['number']
            if str(album_id) in existing_numbers_dict:
                album_number_obj = existing_numbers_dict[str(album_id)]
                album_number_obj.number = number
                album_number_obj.save()
                updated_numbers.append(album_number_obj)
                del existing_numbers_dict[str(album_id)]
            else:
                current_album = Album.objects.get(pk=album_id)
                album_number_obj = AlbumSong.objects.create(
                    album=current_album,
                    number=number
                )
                updated_numbers.append(album_number_obj)
        for album_number_obj in existing_numbers_dict.values():
            album_number_obj.delete()
        instance.album_numbers.set(updated_numbers)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        album_numbers = representation['album_numbers']
        album_numbers = [
            f"{Album.objects.get(pk=album['album'])}  №{album['number']}"
            for album in album_numbers
        ]
        representation['album_numbers'] = album_numbers
        return representation
