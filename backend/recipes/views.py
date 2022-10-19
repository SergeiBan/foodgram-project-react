from rest_framework import viewsets, permissions, status, mixins, filters
from recipes.models import Recipe, Ingredient, Tag, Favorite, Cart
from recipes.serializers import (
    PostRecipeSerializer, RecipeSerializer, IngredientSerializer,
    TagSerializer, ChooseRecipeSerializer)
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from core.pagination import CustomizedPagination
from recipes.permissions import AuthorOrAuthenticatedElseReadOnly


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomizedPagination
    permission_classes = [AuthorOrAuthenticatedElseReadOnly]

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return RecipeSerializer
        else:
            return PostRecipeSerializer
    
    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'tags', 'favorite', 'cart').all()
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        author = self.request.query_params.get('author')
        tags = self.request.query_params.getlist('tags')
        
        if is_favorited == '1':
            recipes = recipes.filter(favorite__user=self.request.user)
        if is_in_shopping_cart == '1':
            recipes = recipes.filter(cart__user=self.request.user)
        if author:
            author = int(author)
            recipes = recipes.filter(author=author)
        if tags:
            for tag in tags:
                tag = Tag.objects.get(slug=tag).pk
                recipes = recipes.filter(tags=tag)
        return recipes


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


class ListRetrieveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class TagViewSet(ListRetrieveViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CreateDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class FavoriteViewSet(CreateDeleteViewSet):
    queryset = Favorite.objects.all()
    serializer_class = ChooseRecipeSerializer

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        try:
            Favorite.objects.get(user=request.user, recipe=recipe).delete()
        except Exception as error:
            raise ValidationError(error)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, serializer, *args, **kwargs):
        id = self.kwargs['id']
        recipe = get_object_or_404(Recipe, pk=id)
        try:
            Favorite.objects.create(user=self.request.user, recipe=recipe)
        except Exception as error:
            raise ValidationError(error)

        serializer = self.serializer_class(recipe)
        return Response(serializer.data)


class ShoppingCartViewSet(CreateDeleteViewSet):
    model = Recipe
    serializer_class = ChooseRecipeSerializer

    def create(self, serializer, *args, **kwargs):
        id = self.kwargs['id']
        recipe = get_object_or_404(Recipe, pk=id)
        try:
            Cart.objects.create(user=self.request.user, recipe=recipe)
        except Exception as error:
            raise ValidationError(error)
        serializer = self.serializer_class(recipe)
        return Response(serializer.data)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        try:
            Cart.objects.get(user=request.user, recipe=recipe).delete()
        except Exception as error:
            raise ValidationError(error)
        
        return Response(status=status.HTTP_204_NO_CONTENT)