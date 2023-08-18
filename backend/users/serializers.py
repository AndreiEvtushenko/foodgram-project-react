from rest_framework import serializers
from django.contrib.auth import get_user_model

from foodgram.models import Recipe
from users.models import Subscription
from utils.validators import password_slug_username_validation

User = get_user_model()


class CreateUserTokenSerializer(serializers.Serializer):
    """
    Serializer for processing POST requests
    from the CreateUserTokenView
    """

    email = serializers.CharField()
    password = serializers.CharField()


class ChangeUserPasswordSerializer(serializers.Serializer):
    """
    Serializer for processing POST requests
    from the ChangeUserPasswordView
    """

    new_password = serializers.CharField()
    current_password = serializers.CharField()

    def validate_new_password(self, value):
        """Method for validating a field while saving the user's password"""

        try:
            password_slug_username_validation(value)
        except serializers.ValidationError as validation_error:
            raise serializers.ValidationError(str(validation_error))

        return value


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    """
    Serializer for processing GET
    request from the SubscriptionSerializer.
    """

    class Meta:
        """Setting input and output fields."""

        fields = (
            'id', 'name', 'image', 'cooking_time'
        )
        model = Recipe


class UserGetSerializer(serializers.ModelSerializer):
    """Serializer for processing GET requests from the UserViewSet"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        """Setting input and output fields"""

        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name',
            'is_subscribed',
        )
        model = User

    def get_is_subscribed(self, obj):
        """
        Method for getting an additional check field
        for the user's subscription to the author
        """

        request = self.context.get('request')
        user = request.user
    
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, author=obj).exists()

        return False


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for processing POST requests from the UserViewSet"""

    class Meta:
        """Setting input and output fields"""

        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'password'
        )
        model = User
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        """Method for validating a field while saving the user's password"""

        try:
            password_slug_validation(value)
        except serializers.ValidationError as validation_error:
            raise serializers.ValidationError(str(validation_error))

        return value


class UserListRetrieveSerializer(serializers.ModelSerializer):
    """Sert"""

    class Meta:
        """Set"""

        fields = (
            'email', 'username', 'first_name',
            'last_name', 'is_superuser'
            # "is_subscribed": false
        )
        model = User


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for processing GET 
    request from the SubscriptionViewSet.
    """

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        """Setting input and output fields."""

        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed',
            'recipes', 'recipes_count'
        )
        model = User

    def get_recipes(self, obj):
        """
        Method for getting recipes of the author
        the user is subscribed.
        """

        recipes = Recipe.objects.filter(author=obj)
        serializer = RecipeMinifiedSerializer(recipes, many=True)

        return serializer.data

    def get_recipes_count(self, obj):
        """
        Method for getting the number of recipes
        of the author the user is following.
        """

        recipes = Recipe.objects.filter(author=obj)
        recipes_count = recipes.count()

        return recipes_count

    def get_is_subscribed(self, obj):
        """
        Method shows if the user is subscribed to the author.
        """

        request = self.context.get('request')
        user = request.user

        return Subscription.objects.filter(user=user, author=obj).exists()
