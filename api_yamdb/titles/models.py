from operator import mod
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    g_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.slug


class Category(models.Model):
    c_name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.slug


class Title(models.Model):
    name = models.TextField(max_length=64)
    year = models.IntegerField("Год выпуска")
    # rating = models.ForeignKey()
    description = models.CharField(max_length=256)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ],
        default=5
    )
    genre = models.ForeignKey(
        Genre,
        null=False,
        blank=False,
        related_name='genres',
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Category,
        null=False,
        blank=False,
        related_name='cat',
        on_delete=models.CASCADE,
    )