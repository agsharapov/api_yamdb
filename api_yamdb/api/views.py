from rest_framework import viewsets
from reviews.models import Category, Genre, Title
from reviews.models import User, Score, Review, Comment
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                           ReviewSerializer, CommentSerializer,
                          UserSerializer, AdminSerializer, SignupSerializer,
                          TokenSerializer) # ScoreSerializer,
from .permissions import AuthorOrReadOnly, Moderator, Admin, ReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
