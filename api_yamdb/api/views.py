from rest_framework import viewsets, filters, status, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from reviews.models import (Category, Genre, Title,
                            User, Review)
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          ReviewSerializer, CommentSerializer, UserSerializer,
                          AdminSerializer, SignupSerializer, TokenSerializer)
from .filters import TitleFilter
from .permissions import AuthorOrReadOnly, Moderator, Admin, ReadOnly


ADMIN_EMAIL = 'robot@yamdb-team.ru'


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (Admin,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('genre', 'genre__slug', 'category__slug')
    search_fields = ('genre', 'genre__slug', 'category__slug',)
    filterset_class = TitleFilter

    def get_queryset(self):
        if 'genre' in self.request.query_params:
            gen = self.request.query_params.get('genre')
            qs = Title.objects.all().prefetch_related(
                Prefetch('genre', queryset=Genre.objects.filter(slug=gen))
            )
        qs = Title.objects.all().select_related('category')
        return qs

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        elif self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (Admin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug',)
    search_fields = ('name', 'slug',)
    lookup_field = ('slug')

    def get_permissions(self):
        if self.action == 'retrieve':
            return (Admin(),)
        elif self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (Admin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug',)
    search_fields = ('name', 'slug',)
    lookup_field = ('slug')

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
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title, author=self.request.user)

    def get_permissions(self):
        if self.action == 'partial_update' or self.action == 'update' or self.action == 'destroy':
            return (AuthorOrReadOnly(), Moderator(), Admin(),)
        if self.action == 'retrieve' or self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):

        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):

        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review, author=self.request.user)

    def get_permissions(self):
        if self.action == 'partial_update' or self.action == 'update' or self.action == 'destroy':
            return (AuthorOrReadOnly(), Moderator(), Admin(),)
        if self.action == 'retrieve' or self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = (Admin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    subject = 'Код подтверждения регистрации на YaMDb'
    message = (
        f'{confirmation_code} — ваш код подтверждения регистрации на YaMDb'
    )
    admin_email = ADMIN_EMAIL
    user_email = [user.email]
    return send_mail(subject, message, admin_email, user_email)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = serializer.data['username']
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.data['confirmation_code']
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    token = RefreshToken.for_user(user)
    return Response(
        {'token': str(token.access_token)}, status=status.HTTP_200_OK
    )


@action(
    detail=False, methods=['GET', 'PATCH'],
    url_path='me', url_name='me',
    permission_classes=(IsAuthenticated,)
)
def user_profile(self, request):
    serializer = UserSerializer(request.user)
    if request.method == 'PATCH':
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.data, status=status.HTTP_200_OK)
