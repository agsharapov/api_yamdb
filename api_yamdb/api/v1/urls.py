from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (TitleViewSet, GenreViewSet, CategoryViewSet,
                       ReviewViewSet, CommentViewSet, UserViewSet,
                       signup, get_token)


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='login'),
]

urlpatterns = [
    path('', include(v1_router.urls), name='api'),
    path('', include(auth)),
]
