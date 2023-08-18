from django.urls import path, include

from rest_framework import routers

from foodgram.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet
)
from users.views import (
    AddDeleteRecipesShoppingCartView,
    AddDeleteUserSubscribeView,
    ChangeUserPasswordView,
    CreateUserTokenView,
    DeleteUserTokenView,
    DownloadShoppingCartView,
    FavoriteView,
    UserMeAPIView,
    UserViewSet,
    SubscriptionViewSet,
)


router = routers.DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('subscriptions', SubscriptionViewSet, basename='subscriptions')
router.register('users', UserViewSet, basename='users')

urlpatterns = [

    path('recipes/', include([
        path(
            'download_shopping_cart/',
            DownloadShoppingCartView.as_view(),
            name='download_shopping_cart'
        ),
        path(
            '<int:id>/favorite/',
            FavoriteView.as_view(),
            name='recipes_favorite'
        ),
        path(
            '<int:id>/shopping_cart/',
            AddDeleteRecipesShoppingCartView.as_view(),
            name='shopping_cart'
        ),
    ])),

    path('auth/', include([
        path(
            'token/login/',
            CreateUserTokenView.as_view(),
            name='creat_token'
        ),
        path(
            'token/logout/',
            DeleteUserTokenView.as_view(),
            name='delete_token'
        ),
    ])),

    path('users/', include([
        path(
            'set_password/',
            ChangeUserPasswordView.as_view(),
            name='set_password'
        ),
        path(
            'me/',
            UserMeAPIView.as_view(),
            name='user_me'
        ),
        path(
            '<int:id>/subscribe/',
            AddDeleteUserSubscribeView.as_view(),
            name='create_subscribe'
        ),
    ])),
    path('', include(router.urls), name='api-root'),
]
