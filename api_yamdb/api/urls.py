from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet, ReviewViewSet, CommentViewSet

router = DefaultRouter()

router.register(
    r'titles', TitleViewSet, basename='titles'
)
router.register(
    r'categories', CategoryViewSet, basename='categories'
)
router.register(
    r'genres', GenreViewSet, basename='genres'
)

router.register(
    r'reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'comments', CommentViewSet, basename='comments'
)
urlpatterns = [
    path('', include(router.urls), name='api'),
]