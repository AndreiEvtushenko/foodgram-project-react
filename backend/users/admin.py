from django.contrib import admin

from .models import Subscription, User, UserFavorite, UserShoppingCart


class SubscriptionInline(admin.TabularInline):
    """
    Subscription inline class for displaying a field
    in the user class in the admin
    """

    model = Subscription
    fk_name = 'user'
    extra = 1


class UserFavoriteInline(admin.TabularInline):
    """
    UserFavorite inline class for displaying a field
    in the user class in the admin
    """

    model = UserFavorite
    fk_name = 'user'
    extra = 1


class UserShoppingCartInline(admin.TabularInline):
    """
    UserShoppingCart inline class for displaying a field
    in the user class in the admin
    """

    model = UserShoppingCart
    fk_name = 'user'
    extra = 1


class UserAdmin(admin.ModelAdmin):
    """User administration"""

    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'display_subscriptions',
        'display_userfavorite',
        'display_usershoppingcart'
    )

    list_display_links = ('username',)

    def display_subscriptions(self, obj):
        """
        Method for the User model in the admin
        to display the user's subscriptions
        """

        subscriptions = obj.subscriptions_follower.all()
        return ', '.join([str(sub.author) for sub in subscriptions])

    def display_userfavorite(self, obj):
        """
        Method for the User model in the admin
        to display the user's favorite recipes
        """

        favorites = obj.user_favorites_user.all()
        return ', '.join([str(sub.recipe) for sub in favorites])

    def display_usershoppingcart(self, obj):
        """
        Method for the User model in the admin
        to display the user's favorite recipes
        """

        usershoppingcart = obj.user_shopping_cart_user.all()
        return ', '.join([str(sub.recipe) for sub in usershoppingcart])

    def save_model(self, request, obj, form, change):
        """
        Override user model save method,
        to properly hash the password before storing.
        """

        if obj.password and not obj.password.startswith('pbkdf2_sha256$'):
            obj.set_password(obj.password)

        super().save_model(request, obj, form, change)

    display_subscriptions.short_description = 'Подписки'
    display_userfavorite.short_description = 'Избранные рецепты'
    display_usershoppingcart.short_description = 'Рецепты в корзине'
    search_fields = ('username', 'email', 'first_name',)
    list_filter = ('username', 'email', 'first_name',)
    empty_value_display = 'пусто'
    inlines = [SubscriptionInline, UserFavoriteInline, UserShoppingCartInline]


admin.site.register(User, UserAdmin)
