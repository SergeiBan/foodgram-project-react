from django.urls import include, path
from recipes.views import (AddRemoveRecipeViewSet, IngredientViewSet,
                           RecipeViewSet, TagViewSet)
from rest_framework.routers import DefaultRouter
from users.views import SubscribeUnsubscribeViewSet, SubscriptionViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'tags', TagViewSet, basename='tag')
router.register(
    r'recipes/(?P<id>\d+)/favorite', AddRemoveRecipeViewSet,
    basename='add_remove_recipe')
router.register(
    r'recipes/(?P<id>\d+)/shopping_cart', AddRemoveRecipeViewSet,
    basename='shopping-add_remove_recipe')
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
