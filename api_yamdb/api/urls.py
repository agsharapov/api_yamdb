from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (TitleViewSet, GenreViewSet, CategoryViewSet,
                       ReviewViewSet, CommentViewSet, UserViewSet,
                       signup, get_token)


from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
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
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments'
)

urlpatterns = [
    path('', include(router.urls), name='api'),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='login'),
    path('api/123/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
