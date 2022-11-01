from operator import mod
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from titles.models import Title

class Score(models.Model):
    value = models.SmallIntegerField(validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        default=0)
    #author= models.ForeignKey(
     #   User, on_delete=models.CASCADE, related_name='scores')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='scores')
    voted_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('author', 'title')


class Review(models.Model):
    # author= models.ForeignKey(
     #   User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    score = models.ForeignKey(Score, on_delete=models.CASCADE, related_name='reviews')

class Comment(models.Model):
    # author= models.ForeignKey(
     #   User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    
