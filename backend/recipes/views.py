from django.db.transaction import atomic
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.pagination import CustomizedPagination
from recipes.mixins import CreateDeleteViewSet, ListRetrieveViewSet
from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag
from recipes.permissions import AuthorOrAuthenticatedElseReadOnly
from recipes.serializers import (ChooseRecipeSerializer, IngredientSerializer,
                                 PostRecipeSerializer, RecipeAddSerializer,
                                 RecipeSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Добавляет рецепт, получает любой рецепт и все рецепты,
    обновляет свои рецепты и удаляет. Позволяет скачать
    список ингредиентов.
    """
    pagination_class = CustomizedPagination
    permission_classes = [AuthorOrAuthenticatedElseReadOnly]

    @atomic
    def create(self, request, *args, **kwargs):
        new_recipe = None
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_recipe = serializer.save()
        output_serializer = RecipeSerializer(
            new_recipe, context={'request': request})
        return Response(output_serializer.data)

    @atomic
    def update(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
        serializer = self.get_serializer(recipe, data=request.data)
        serializer.is_valid(raise_exception=True)
        new_recipe = serializer.save()
        output_serializer = RecipeSerializer(
            new_recipe, context={'request': request})
        return Response(output_serializer.data)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return RecipeSerializer
        return PostRecipeSerializer

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'tags', 'favorite', 'cart').all()
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        author = self.request.query_params.get('author')
        author = int(author) if author and author.isdecimal() else None
        tags = self.request.query_params.getlist('tags')

        if is_favorited == '1':
            recipes = recipes.filter(favorite__user=self.request.user)
        if is_in_shopping_cart == '1':
            recipes = recipes.filter(cart__user=self.request.user)
        if author:
            recipes = recipes.filter(author=author)
        if tags:
            return recipes.filter(tags__slug__in=tags).distinct()
        return recipes

    @action(detail=False, url_path='download_shopping_cart')
    def download(self, request):
        download_data = Cart.get_shopping_list(request.user)
        return FileResponse(
            download_data, as_attachment=True, filename='Покупки.pdf')


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Выводит список ингредиентов и отдельный ингредиент.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']
    pagination_class = None


class TagViewSet(ListRetrieveViewSet):
    """
    Выводит список тэгов и отдельный тэг.
    """
    permission_classes = (permissions.AllowAny,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class AddRemoveRecipeViewSet(CreateDeleteViewSet):
    """
    Добавляет и удаляет рецепт из/в избранное либо в корзину.
    В зависимости от URL.
    """
    queryset = Favorite.objects.all()
    serializer_class = RecipeAddSerializer

    def delete(self, request, id):
        model = Cart
        if 'favorite' in request.get_full_path():
            model = Favorite
        id = self.kwargs['id']
        serializer = self.get_serializer(data=self.request.data, context={
            'request': self.request, 'model': model, 'id': id})
        serializer.is_valid(raise_exception=True)
        recipe = get_object_or_404(Recipe, pk=id)
        model.objects.get(user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, *args, **kwargs):
        model = Cart
        if 'favorite' in self.request.get_full_path():
            model = Favorite
        id = self.kwargs['id']
        serializer = self.get_serializer(data=self.request.data, context={
            'request': self.request, 'model': model, 'id': id})
        serializer.is_valid(raise_exception=True)
        recipe = get_object_or_404(Recipe, pk=id)
        model.objects.create(user=self.request.user, recipe=recipe)
        serializer = ChooseRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
