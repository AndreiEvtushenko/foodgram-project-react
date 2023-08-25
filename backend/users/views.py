from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse

from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from foodgram.models import Recipe
from users.models import Subscription, UserFavorite, UserShoppingCart
from users.serializers import (
    ChangeUserPasswordSerializer,
    CreateUserTokenSerializer,
    SubscriptionSerializer,
    UserGetSerializer,
    UserCreateSerializer
)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset for processing requests:
    a list of users GET /api/users/
    search user by id GET /api/users/id
    user creation POST /api/users/
    """

    queryset = User.objects.all()

    def get_permissions(self):
        """Selecting a permissions depending on the request"""

        if self.action == 'list':
            return [IsAuthenticated()]
        elif self.action in ['retrieve', 'create']:
            return [AllowAny()]

    def get_serializer_class(self):
        """Selecting a serializer depending on the request"""

        if self.request.method == 'GET':
            return UserGetSerializer

        return UserCreateSerializer

    def perform_create(self, serializer):
        """Method creates a user in the database"""

        password = serializer.validated_data['password']
        user = serializer.save()
        user.set_password(password)
        user.save()


class CreateUserTokenView(APIView):
    """
    View for processing requests:
    to get user token POST 'api/auth/token/login/'
    """

    permission_classes = [AllowAny, ]

    def post(self, request):
        """" Method for getting and saving a token for a user"""

        serializer = CreateUserTokenSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            password = validated_data['password']
            email = validated_data['email']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {'message': 'Пользователь не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )

            if not check_password(password, user.password):
                return Response(
                    {'message': 'Неверный пароль'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                old_token = Token.objects.get(user=user)
                if old_token:
                    return Response(
                        {'auth_token': old_token.key},
                        status=status.HTTP_200_OK
                    )
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
                return Response(
                    {'auth_token': token.key},
                    status=status.HTTP_200_OK
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DeleteUserTokenView(APIView):
    """
    View for processing requests:
    to delete user token POST 'api/auth/token/logout/'
    """

    def post(self, request):
        """Method delete user token"""

        user = self.request.user
        try:
            old_token = Token.objects.get(user=user)
            old_token.delete()
        except Token.DoesNotExist:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeUserPasswordView(APIView):
    """
    View for processing requests:
    user password change
    POST api/users/set_password/
    """

    def post(self, request):
        """Method to change user password"""

        serializer = ChangeUserPasswordSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            new_password = validated_data['new_password']
            current_password = validated_data['current_password']
            user = self.request.user

            if not check_password(current_password, user.password):
                return Response(
                    {'message': 'Неверный пароль'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserMeAPIView(APIView):
    """
    APIView for processing requests:
    users/me/
    """

    def get(self, request):
        """
        Method for calling the serializer and passing
        the context with the data from the request
        """

        user = request.user
        serializer = UserGetSerializer(user, context={'request': request})
        return Response(serializer.data)


class FavoriteView(APIView):
    """
    Viewset for processing requests:
    add recipe in favorite by id POST /api/recipes/id/favorite/
    delete recipe from favorite by id POST /api/recipes/id/favorite/
    """

    def post(self, request, id):
        """Method adds recipe in favorite"""

        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            raise NotFound(detail='Рецепт не найден')

        user = self.request.user

        try:
            UserFavorite.objects.get(recipe=recipe, user=user)
            return Response(
                {'message': 'Рецепт уже в избранном'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except UserFavorite.DoesNotExist:
            UserFavorite.objects.create(recipe=recipe, user=user)

            return Response(
                {'message': 'Рецепт успешно добавлен в избранное'},
                status=status.HTTP_201_CREATED
            )

    def delete(self, request, id):
        """Method deletes recipe from favorite"""

        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            raise NotFound(detail='Рецепт не найден')

        user = self.request.user

        try:
            favorite = UserFavorite.objects.get(recipe=recipe, user=user)
        except UserFavorite.DoesNotExist:
            raise NotFound(detail='Рецепт не найден в избранном')

        favorite.delete()
        return Response(
            {'message': 'Рецепт успешно удален из избранного'},
            status=status.HTTP_204_NO_CONTENT
        )


class AddDeleteRecipesShoppingCartView(APIView):
    """
    Viewset for processing requests:
    add recipe in shopping cart POST api/recipes/id/shopping_cart/
    delete recipe from shopping cart DEL api/recipes/id/shopping_cart/
    """

    def post(self, request, id):
        """Method adds recipe in shopping cart"""

        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            return Response(
                {'message': 'Рецепт не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        user = self.request.user

        try:
            UserShoppingCart.objects.get(recipe=recipe, user=user)
            return Response(
                {'message': 'Рецепт уже в избранном'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except UserShoppingCart.DoesNotExist:
            UserShoppingCart.objects.create(recipe=recipe, user=user)

            return Response(
                {'message': 'Рецепт успешно добавлен в избранное'},
                status=status.HTTP_201_CREATED
            )

    def delete(self, request, id):
        """Method deletes recipe from shopping cart"""

        try:
            recipe = Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            raise NotFound(detail='Рецепт не найден')

        user = self.request.user

        try:
            shopping_cart = UserShoppingCart.objects.get(
                recipe=recipe, user=user
            )
        except UserShoppingCart.DoesNotExist:
            raise NotFound(detail='Рецепт не найден в корзине')

        shopping_cart.delete()
        return Response(
            {'message': 'Рецепт успешно удален из корзины'},
            status=status.HTTP_204_NO_CONTENT
        )


class DownloadShoppingCartView(APIView):
    """
    View for processing requests:
    download shopping cart GET recipes/download_shopping_cart/
    """

    def get(self, request):
        """
        Method for generating and sending
        a text file with a list of recipes
        """

        user = request.user
        shopping_list = UserShoppingCart.objects.filter(user=user)

        shopping_cart_content = ""

        for recipe_cart in shopping_list:
            recipe = recipe_cart.recipe
            shopping_cart_content += f"Recipe: {recipe.name}\n"
            shopping_cart_content += "Ingredients:\n"
            for ingredient in recipe.ingredients.all():
                recipe_ingredient = recipe.recipeingredient_set.first().amount
                shopping_cart_content += (
                    f" - {ingredient.name} {recipe_ingredient} {ingredient.measurement_unit}\n"
                )
            shopping_cart_content += (
                f"Cooking Time: {recipe.cooking_time} minutes\n"
            )
            shopping_cart_content += f"Description: {recipe.text}\n\n"

        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        response.write(shopping_cart_content)
        return response


class AddDeleteUserSubscribeView(APIView):
    """
    Viewset for processing requests:
    add subscribe POST api/recipes/id/shopping_cart/
    delete subscribe DEL api/recipes/id/shopping_cart/
    """

    def post(self, request, id):
        """Method adds a subscription to the author"""

        try:
            author = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {'message': 'Автор не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        seralizer = SubscriptionSerializer(
            author, context={'request': request}
        )
        user = self.request.user

        if author == user:
            return Response(
                {'message': 'Невозможно подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            Subscription.objects.get(author=author, user=user)
            return Response(
                {'message': 'Вы уже подписаны на автора'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Subscription.DoesNotExist:
            Subscription.objects.create(author=author, user=user)

            return Response(seralizer.data)

    def delete(self, request, id):
        """Method delete a subscription to the author"""

        try:
            author = User.objects.get(id=id)
        except User.DoesNotExist:
            raise NotFound(detail='Автор не найден')

        user = self.request.user

        try:
            subscription = Subscription.objects.get(
                author=author, user=user
            )
        except Subscription.DoesNotExist:
            raise NotFound(detail='Вы ещё не подписаны на этого автора')

        subscription.delete()
        return Response(
            {'message': 'Вы больше не подписаны на этого автора'},
            status=status.HTTP_204_NO_CONTENT
        )


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    Viewset for processing requests:
    a list of Subscriptions GET /api/users/subscriptions/
    """

    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        """Method for getting user's subscriptions"""

        user = self.request.user
        queryset = user.subscriptions_follower.all()
        queryset = [subscription.author for subscription in queryset]
        return queryset
