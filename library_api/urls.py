from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# ViewSets
from authors.routes.author import AuthorViewSet
from books.routes.book import BookViewSet
from favorite.routes.favorite import FavoriteViewSet

# Auth-related views
from user.routes.user import RegisterView
from login.routes.login import LoginView
from logout.routes.logout import LogoutView

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'favorites', FavoriteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/favorites/recommendations/', FavoriteViewSet.as_view({'get': 'recommendations'}), name='favorite-recommendations'),
]
