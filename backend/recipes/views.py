from rest_framework import viewsets, permissions, status, mixins, filters, decorators
from recipes.models import Recipe, Ingredient, Tag, Favorite, Cart
from recipes.serializers import (
    PostRecipeSerializer, RecipeSerializer, IngredientSerializer,
    TagSerializer, ChooseRecipeSerializer)
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from core.pagination import CustomizedPagination
from recipes.permissions import AuthorOrAuthenticatedElseReadOnly, AdminOnlyUnsafe
import io
from django.http import FileResponse
from weasyprint import HTML
from django.db import transaction


# @transaction.atomic
class RecipeViewSet(viewsets.ModelViewSet):
    """
    Добавляет рецепт, получает любой рецепт и все рецепты,
    обновляет свои рецепты и удаляет. Позволяет скачать
    список ингредиентов.
    """
    queryset = Recipe.objects.all()
    pagination_class = CustomizedPagination
    permission_classes = [AuthorOrAuthenticatedElseReadOnly]

    def create(self, request, *args, **kwargs):
        new_recipe = None
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_recipe = serializer.save()
        output_serializer = RecipeSerializer(
            new_recipe, context={'request': request})
        return Response(output_serializer.data)

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

    @action(detail=False, url_path='download_shopping_cart')
    def download(self, request):
        buffer = io.BytesIO()

        total = {}
        cart_content = request.user.cart.prefetch_related(
            'recipe__ingredients').all()
        for cart_record in cart_content:
            ingredients = cart_record.recipe.ingredients.all()
            for ingredient in ingredients:
                if total.get(ingredient.ingredient):
                    total[ingredient.ingredient] += ingredient.amount
                else:
                    total[ingredient.ingredient] = ingredient.amount

        html_string = '<table><tr><th>Ингредиент</th><th>Количество</th></tr>'
        for key, val in total.items():
            html_string += f'<tr><td>{key}:</td><td>{val}</td></tr>'
        html_string += '</table>'

        HTML(string=html_string).write_pdf(buffer)

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='Покупки.pdf')


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
