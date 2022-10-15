from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipes.views import RecipeViewSet, IngredientViewSet, TagViewSet, FavoriteViewSet, ShoppingCartViewSet
from rest_framework.authtoken import views
from users.views import UserViewSet, SubscriptionViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'tags', TagViewSet, basename='tag')
router.register(
    r'recipes/(?P<id>\d+)/favorite', FavoriteViewSet, basename='favorite')
router.register(r'recipes/(?P<id>\d+)/shopping_cart', ShoppingCartViewSet, basename='shopping-cart')
router.register(r'users/subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'user/(?P<id>\d+)/subscriptions', viewset)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    
    path('', include(router.urls)),
    path('', include('djoser.urls')),
]
