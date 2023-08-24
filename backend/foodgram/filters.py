from django_filters import rest_framework as filters

from foodgram.models import Ingredient, Recipe


class RecipeFilterSet(filters.FilterSet):
    """
    Custom filterset for filtering by fields:
    author, tags, is_in_shopping_cart, is_favorited.
    """

    is_favorited = filters.NumberFilter(
        field_name='user_favorites_recipe__user',
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.NumberFilter(
        field_name='user_shopping_cart_recipe__user',
        method='filter_is_in_shopping_cart'
    )
    tags = filters.CharFilter(field_name='tags__slug')
    author = filters.NumberFilter(field_name='author__id')

    class Meta:
        """Fields settings."""

        model = Recipe
        fields = ('author', 'tags', 'is_in_shopping_cart', 'is_favorited')

    def filter_is_favorited(self, queryset, name, value):
        """Method for filtering by an additional field."""

        if value:
            return queryset.filter(
                user_favorites_recipe__user=self.request.user
            )
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """Method for filtering by an additional field."""

        if value:
            return queryset.filter(
                user_shopping_cart_recipe__user=self.request.user
            )
        return queryset


class IngredientFilterSet(filters.FilterSet):
    """Custom filterset for filtering by name."""

    name = filters.CharFilter(field_name='name', method='filter_name')

    def filter_name(self, queryset, name, value):
        """Method for filtering by partial occurrence."""

        return queryset.filter(name__istartswith=value)

    class Meta:
        """Fields settings."""

        model = Ingredient
        fields = ('name', )
