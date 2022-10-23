from django.contrib import admin
from recipes.models import (
    Recipe, Tag, Ingredient, Favorite, RecipeIngredient, Cart)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('favorite_count',)
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')

    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    def get_fields(self, request, obj=None):
        if obj:
            fields = super().get_fields(request, obj=obj)
        else:
            fields = super().get_fields(request, obj=obj)
            fields.remove('favorite_count')
        return fields


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount')


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Cart, CartAdmin)
