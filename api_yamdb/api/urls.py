from django.urls import path, include
from rest_framework.routers import DefaultRouter
# efimov - для тестов 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) # efimov - для тестов 


from api.views import (TitleViewSet, GenreViewSet, CategoryViewSet,
                       ReviewViewSet, CommentViewSet, UserViewSet)

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
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments'
)
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls), name='api'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # efimov - для тестов 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # efimov - для тестов 
]
