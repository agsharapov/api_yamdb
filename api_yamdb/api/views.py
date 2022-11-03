from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Category, Genre, Title
from reviews.models import User, Score, Review, Comment
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                           ReviewSerializer, CommentSerializer,
                          UserSerializer, AdminSerializer, SignupSerializer,
                          TokenSerializer) # ScoreSerializer,
from .permissions import AuthorOrReadOnly, Moderator, Admin, ReadOnly

from rest_framework.response import Response
from rest_framework import status


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    #permission_classes = (ReadOnly,)
    def perform_create(self, serializer):
        print(serializer.data['genre'])
        print(serializer)
        serializer.save(
            genre=Genre.objects.get(slug=serializer.data['genre']),
            category=Category.objects.get(slug=self.kwargs.get('category'))
        )

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (Admin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name','slug',) 
    search_fields = ('name', 'slug',) 

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        elif self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()
    
    def delete(self, request, slug):
        event = self.get_object(slug)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (Admin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name','slug',) 
    search_fields = ('name', 'slug',) 


    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        elif self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
