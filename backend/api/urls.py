from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import RecipeViewSet
from rest_framework.authtoken import views

app_name = 'api'

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('auth/token/login/', views.obtain_auth_token),
    path('', include('djoser.urls')),
    path('', include(router.urls))
]
