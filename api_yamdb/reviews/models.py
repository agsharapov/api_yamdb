from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from datetime import datetime


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
USER_ROLE_CHOICES = [
    ('user', USER),
    ('moderator', MODERATOR),
    ('admin', ADMIN)
]

ALPHANUMERIC = RegexValidator(
    r'^[0-9a-zA-Z]*$', 'Допустимы только буквы или цифры.'
)
REVIEW_TEXT_LENGTH = 15


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    role = models.CharField(
        max_length=255,
        choices=USER_ROLE_CHOICES,
        default=USER,
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    score = models.SmallIntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]

    def __str__(self):
        return self.text[:REVIEW_TEXT_LENGTH]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        unique=True, max_length=50, validators=[ALPHANUMERIC],
    )

    def __str__(self) -> str:
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True, max_length=50, validators=[ALPHANUMERIC],
    )

    def __str__(self) -> str:
        return self.slug


class TitleGenre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE, related_name='titles'
    )

    def __str__(self):
        return f'{self.title} {self.genre}'


class Title(models.Model):
    name = models.TextField(max_length=64, blank=False)

    year = models.IntegerField(
        "Год выпуска",
        validators=[MinValueValidator(0),
                    MaxValueValidator(datetime.now().year)]
    )
    description = models.CharField(max_length=256)
    genre = models.ManyToManyField(
        Genre, through=TitleGenre, related_name='genre'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        related_name='category',
        on_delete=models.CASCADE,
    )
