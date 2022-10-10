from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import RecipeViewSet
from rest_framework.authtoken import views
from users.views import UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/token/login/', views.obtain_auth_token),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
