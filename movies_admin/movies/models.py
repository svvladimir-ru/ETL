from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PersonRole(models.TextChoices):
    DIRECTOR = 'director', _('директор')
    WRITER = 'writer', _('сценарист')
    ACTOR = 'actor', _('актер')


class FilmWorkType(models.TextChoices):
    MOVIE = 'movie', _('фильм')
    TV_SHOW = 'tv_show', _('шоу')


class FilmWork(TimeStampedMixin):
    id = models.UUIDField(primary_key=True)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateField(null=True)
    certificate = models.TextField(blank=True, null=True)
    file_path = models.FileField(upload_to='film_works/', blank=True, null=True)
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        blank=True, null=True
    )
    type = models.CharField(max_length=30, choices=FilmWorkType.choices, default=FilmWorkType.MOVIE)
    genres = models.ManyToManyField('Genre', through='GenreFilmWork')
    persons = models.ManyToManyField('Person', through='PersonFilmWork')

    class Meta:
        managed = False
        db_table = 'film_work'


class Genre(TimeStampedMixin):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, max_length=30)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genre'


class GenreFilmWork(models.Model):
    id = models.UUIDField(primary_key=True)
    film_work = models.ForeignKey(FilmWork, models.DO_NOTHING)
    genre = models.ForeignKey(Genre, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'genre_film_work'
        unique_together = (('film_work', 'genre'),)


class Person(TimeStampedMixin):
    id = models.UUIDField(primary_key=True)
    full_name = models.CharField(max_length=40)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'


class PersonFilmWork(models.Model):
    id = models.UUIDField(primary_key=True)
    film_work = models.ForeignKey(FilmWork, models.DO_NOTHING)
    person = models.ForeignKey(Person, models.DO_NOTHING)
    role = models.CharField(max_length=20, choices=PersonRole.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'person_film_work'
        unique_together = (('film_work', 'person', 'role'),)
