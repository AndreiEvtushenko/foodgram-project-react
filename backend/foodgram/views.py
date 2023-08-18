from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from foodgram.filters import RecipeFilterSet
from foodgram.permissions import ChangeObjectIfAuthor
from foodgram.utils.save_ingredients import save_ingredients_for_resipe
from foodgram.utils.save_tags import save_tags_for_recipes
from foodgram.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer
)
from foodgram.models import Ingredient, Recipe, Tag


User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for processing requests:
    a list of ingredients GET /api/ingredients/
    get ingredient by id GET /api/ingredients/id/
    """

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for processing requests:
    a list of tags GET /api/tags/
    get tag by id GET /api/tags/id/
    """

    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Viewset for processing requests:
    a list of recipes GET /api/recipes/
    get recipe by id GET /api/recipes/id/
    create recipe POST /api/recipes/
    delete recipe by id DELETE /api/recipes/id/
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet

    def get_permissions(self):
        """Selecting a permissions depending on the request"""

        if self.action in ['retrieve', 'list']:
            return [AllowAny()]
        return [ChangeObjectIfAuthor(), IsAdminUser()]

    def perform_create(self, serializer):
        """Method creates a recipe with ingredients and tags"""

        recipe = serializer.save(author=self.request.user)

        ingredients_data = self.request.data.get('ingredients')
        tags_data = self.request.data.get('tags')

        if ingredients_data:
            save_ingredients_for_resipe(ingredients_data, recipe)

        if tags_data:
            save_tags_for_recipes(tags_data, recipe)

    def partial_update(self, request, *args, **kwargs):
        """Method changes a recipe with ingredients and tags"""

        recipe = self.get_object()
        ingredients_data = self.request.data.get('ingredients')
        tags_data = self.request.data.get('tags')

        if ingredients_data:
            recipe.ingredients.clear()
            save_ingredients_for_resipe(ingredients_data, recipe)

        if tags_data:
            recipe.tags.clear()
            save_ingredients_for_resipe(ingredients_data, recipe)

        serializer = self.get_serializer(
            recipe, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
