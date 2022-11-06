from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


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
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='scores')
    title = models.ForeignKey('Title', on_delete=models.CASCADE,
                              related_name='scores')
    voted_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('author', 'title')


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    score = models.ForeignKey(Score, on_delete=models.CASCADE,
                              related_name='reviews')


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
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.slug


class TitleGenre(models.Model):
    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE, related_name='titles'
    )
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class TitleCategory(models.Model):
    title = models.ForeignKey('Title', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.category}'


class Title(models.Model):
    name = models.TextField(max_length=64, blank=False)
    year = models.IntegerField("Год выпуска")
    # rating = models.ForeignKey()
    description = models.CharField(max_length=256)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        default=5
    )
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
