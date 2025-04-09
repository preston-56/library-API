from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# ViewSets
from authors.routes.author import AuthorViewSet
from books.routes.book import BookViewSet
from favorite.routes.favorite import FavoriteViewSet

# Auth-related views
from user.routes.user import RegisterView
from login.routes.login import LoginView
from logout.routes.logout import LogoutView

router = DefaultRouter()
router.register(r"authors", AuthorViewSet)
router.register(r"books", BookViewSet)
router.register(r"favorites", FavoriteViewSet)

# Swagger schema view setup
schema_view = get_schema_view(
    openapi.Info(
        title="Library API",
        default_version="v1",
        description="API documentation for the Library project",
        contact=openapi.Contact(email="prestonosoro56@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),

    # Alias for accounts/logout
    # path('accounts/logout/', LogoutView.as_view(), name='logout'),

    # Swagger and Redoc
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
