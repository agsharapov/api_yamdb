from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Category, Genre, Title
from reviews.models import User, Review, Comment
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                           ReviewSerializer, CommentSerializer,
                          UserSerializer, AdminSerializer, SignupSerializer,
                          TokenSerializer) 
from .permissions import AuthorOrReadOnly, Moderator, Admin, ReadOnly
from django.shortcuts import get_object_or_404
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
    serializer_class = ReviewSerializer
  
    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title, author=self.request.user)

    def get_permissions(self):
        if self.action == 'partial_update' or self.action == 'update' or self.action == 'destroy':
            return (AuthorOrReadOnly(), Moderator(), Admin(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
   
    serializer_class = CommentSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return title.review.comments

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(title=title, review=review, author=self.request.user)

    def get_permissions(self):
        if self.action == 'partial_update' or self.action == 'update' or self.action == 'destroy':
            return (AuthorOrReadOnly(), Moderator(), Admin(),)
        return super().get_permissions()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
