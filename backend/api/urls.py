from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipes.views import (
    RecipeViewSet, IngredientViewSet, TagViewSet, FavoriteViewSet,
    ShoppingCartViewSet)
from users.views import SubscriptionViewSet, SubscribeUnsubscribeViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'tags', TagViewSet, basename='tag')
router.register(
    r'recipes/(?P<id>\d+)/favorite', FavoriteViewSet, basename='favorite')
router.register(
    r'recipes/(?P<id>\d+)/shopping_cart', ShoppingCartViewSet,
    basename='shopping-cart')
router.register(
    r'users/subscriptions', SubscriptionViewSet, basename='subscription')
router.register(
    r'users/(?P<id>\d+)/subscribe', SubscribeUnsubscribeViewSet,
    basename='subscribe')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
