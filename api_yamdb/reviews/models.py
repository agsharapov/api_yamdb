from operator import mod
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from titles.models import Title

USER_ROLE_CHOICES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    role = models.CharField(
        max_length=255,
        choices=USER_ROLE_CHOICES,
        default='user',
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
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'


class Score(models.Model):
    value = models.SmallIntegerField(validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        default=0)
    author= models.ForeignKey(
       User, on_delete=models.CASCADE, related_name='scores')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='scores')
    voted_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('author', 'title')


class Review(models.Model):
    author= models.ForeignKey(
       User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    score = models.ForeignKey(Score, on_delete=models.CASCADE, related_name='reviews')

class Comment(models.Model):
    author= models.ForeignKey(
       User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    
