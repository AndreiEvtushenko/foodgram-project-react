from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import models

from utils.validators import password_slug_username_validation


MAX_LENGTH_50: int = 50
MAX_LENGTH_150: int = 150
MAX_LENGTH_250: int = 250
MAX_LENGTH_254: int = 254


class User(AbstractUser):
    """Modified user model"""

    first_name = models.CharField(
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя',
        max_length=MAX_LENGTH_150,
        blank=False
    )

    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        help_text='Введите фамилию пользователя',
        max_length=MAX_LENGTH_150,
        blank=False
    )

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text=(
            'Введите адрес электронной почты, '
            'поле обязательное для заполнения'
        ),
        blank=False,
        max_length=MAX_LENGTH_254,
        validators=[EmailValidator],
        unique=True
    )

    username = models.CharField(
        verbose_name='Уникальное имя пользователя',
        help_text='Введите username',
        blank=False,
        max_length=MAX_LENGTH_150,
        validators=[password_slug_username_validation],
        unique=True
    )

    password = models.CharField(
        verbose_name='Пароль пользователя',
        help_text=(
            'Введите пароль, '
            'это обязательное поле'
        ),
        max_length=MAX_LENGTH_150,
        blank=False
    )

    subscription = models.ManyToManyField(
        'self',
        through='Subscription',
        symmetrical=False,
        related_name='subscriptions',
        verbose_name='Подписки автора',
        help_text='На кого подписан автор'
    )

    favorite = models.ManyToManyField(
        'foodgram.Recipe',
        through='UserFavorite',
        related_name='user_favorites',
        verbose_name='Избранные рецепты',
        help_text='Избраннные рецепты автора'
    )

    shopping_cart = models.ManyToManyField(
        'foodgram.Recipe',
        through='UserShoppingCart',
        related_name='user_shopping_cart',
        verbose_name='Список покупок',
        help_text='Список покупок'
    )

    class Meta:
        """User model settings."""

        ordering = ['username', ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    """Model for linking users Recipe and authors."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions_follower',
        verbose_name='Подписан',
        help_text='Пользователь'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions_following',
        verbose_name='Автор'
    )

    pub_date = models.DateField(auto_now=True)

    class Meta():
        """
        Subscription model settings.
        Unable to follow author twice.
        """

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_subscription_author'
            )
        ]

        ordering = ['user', ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def clean(self):
        if self.user == self.author:
            raise ValidationError('Нельзя подписаться на самого себя')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """String representation of the class"""
        return (
            f'Пользоаватель {self.user} подписан на пользователя {self.author}'
        )


class UserFavorite(models.Model):
    """Model for linking users Recipe and authors."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_favorites_user',
        verbose_name='Избранные рецепты',
        help_text='Избранные рецепты'
    )

    recipe = models.ForeignKey(
        'foodgram.Recipe',
        on_delete=models.CASCADE,
        related_name='user_favorites_recipe',
        verbose_name='Рецепт'
    )

    pub_date = models.DateField(auto_now=True)

    class Meta():
        """
        Subscription model settings.
        Unable to follow author twice.
        """

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_favorite_recipe'
            )
        ]

        ordering = ['pub_date', ]
        verbose_name = 'Избранные'
        verbose_name_plural = 'Избранные'

    def __str__(self) -> str:
        """String representation of the class"""
        return (
            f'Рецепт {self.recipe} в избранном'
        )


class UserShoppingCart(models.Model):
    """Model for linking users Recipe and authors."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_shopping_cart_user',
        verbose_name='Избранные рецепты',
        help_text='Избранные рецепты'
    )

    recipe = models.ForeignKey(
        'foodgram.Recipe',
        on_delete=models.CASCADE,
        related_name='user_shopping_cart_recipe',
        verbose_name='Рецепт'
    )

    pub_date = models.DateField(auto_now=True)

    class Meta():
        """
        Subscription model settings.
        Unable to follow author twice.
        """

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_shopping_cart_recipe'
            )
        ]

        ordering = ['pub_date', ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self) -> str:
        """String representation of the class"""
        return (
            f'Рецепт {self.recipe} в списке покупок'
        )
