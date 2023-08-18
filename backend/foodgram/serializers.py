import base64
from django.core.files.base import ContentFile
from rest_framework import serializers

from foodgram.models import Ingredient, Recipe, Tag
from users.models import UserFavorite, UserShoppingCart
from users.serializers import UserGetSerializer
from utils.validators import (
    hex_name_color_validator,
    password_slug_username_validation
)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for processing GET requests from the IngredientViewSet"""

    class Meta():
        """Setting input and output fields"""

        fields = ('__all__')
        model = Ingredient


class IngredientWithAmountSerializer(serializers.ModelSerializer):
    """Serializer for processing GET requests from the RecipeSerializer"""

    amount = serializers.SerializerMethodField()

    class Meta():
        """Setting input and output fields"""

        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = Ingredient

    def get_amount(self, obj):
        """
        Method for getting an additional field
        for the resipe's amount of ingredient
        """

        recipe_ingredient = obj.recipeingredient_set.first()

        if recipe_ingredient:
            return recipe_ingredient.amount
        return None


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for processing GET requests
    from the TagViewSet
    """

    class Meta:
        """Setting input and output fields"""

        fields = ('id', 'name', 'color', 'slug')
        model = Tag

    def validate_slug(self, value):
        """Method for validating a field slug"""

        try:
            password_slug_username_validation(value)
        except serializers.ValidationError as validation_error:
            raise serializers.ValidationError(str(validation_error))

        return value

    def validate_color(self, value):
        """Method for validating a field color"""

        try:
            hex_name_color_validator(value)
        except serializers.ValidationError as validation_error:
            raise serializers.ValidationError(str(validation_error))

        return value


class Base64ImageField(serializers.ImageField):
    """Serializer for passing images via json format"""

    def to_internal_value(self, data):
        """Set"""

        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for processing GET, POST, PATCH, DELETE
    requests from the RecipeViewSet
    """

    tags = TagSerializer(read_only=True, many=True)
    author = UserGetSerializer(read_only=True)
    ingredients = IngredientWithAmountSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        """Setting input and output fields"""

        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )
        model = Recipe

    def get_is_favorited(self, obj):
        """
        Method for getting an additional field
        for the user's favorites
        """

        request = self.context.get('request')
        user = request.user
        is_favorited = UserFavorite.objects.filter(user=user, recipe=obj)

        if is_favorited:
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        """
        Method for getting an additional field
        for the user's shopping_cart
        """

        request = self.context.get('request')
        user = request.user
        is_in_shopping_cart = UserShoppingCart.objects.filter(
            user=user, recipe=obj
        )

        if is_in_shopping_cart:
            return True
        return False
