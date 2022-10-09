from django.shortcuts import render
from rest_framework import viewsets
from recipes.models import Recipe
from api.serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer