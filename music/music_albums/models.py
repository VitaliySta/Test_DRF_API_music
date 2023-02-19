from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Performer(models.Model):
    """A model representing an artist or a band."""

    title = models.CharField(
        max_length=250,
        unique=True,
        verbose_name='Название исполнителя',
        db_index=True
    )

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Album(models.Model):
    """A model representing an album."""

    performer = models.ForeignKey(
        Performer,
        on_delete=models.CASCADE,
        related_name='albums',
        verbose_name='Исполнитель'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='год выпуска',
        validators=[
            MinValueValidator(
                0,
                message='Значение года не может быть отрицательным'
            ),
            MaxValueValidator(
                int(datetime.now().year),
                message='Значение года не может быть больше текущего'
            )
        ],
        db_index=True
    )

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
        ordering = ('year',)
        constraints = [
            models.UniqueConstraint(
                fields=['performer', 'year'],
                name='unique_performer_year'
            )
        ]

    def __str__(self):
        return f'{self.performer} - {self.year}'


class Song(models.Model):
    """A model representing a song."""

    title = models.CharField(
        max_length=250,
        unique=True,
        verbose_name='Название песни',
        db_index=True
    )
    album_numbers = models.ManyToManyField(
        'AlbumSong',
        related_name='songs',
        verbose_name='Номер в альбоме'
    )

    class Meta:
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'

    def __str__(self):
        return f'{self.title} - {self.album_numbers}'


class AlbumSong(models.Model):
    """A model representing the association between an album and a song."""

    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='albumsong'
    )
    number = models.PositiveSmallIntegerField(
        verbose_name='номер',
        validators=[
            MinValueValidator(
                0,
                message='Значение не может быть отрицательным'
            ),
            MaxValueValidator(
                100,
                message='Значение не может быть больше 100'
            )
        ],
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['album', 'number'], name='unique_number'
            )
        ]

    def __str__(self):
        return f'{self.album} - {self.number}'
