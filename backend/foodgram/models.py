from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from utils.validators import hex_name_color_validator


MIN_VALUE_1 = 1
MAX_LENGTH_7 = 7
MAX_LENGTH_200 = 200
MAX_VALUE_1440 = 1440
MAX_VALUE_10000 = 10000
MIN_VALIDATOR_ERROR_MESSAGE = 'Можно ввести только целое, положительное число'
MAX_VALIDATOR_ERROR_MESSAGE = (
    'Максимальное время приготовления не может превышать 1440 минут'
)
MAX_VALIDATOR_AMOUNT_ERROR_MESSAGE = (
    'Максимальное значение не должно превышать 10000'
)


def validate_non_empty(value):
    if value.count() == 0:
        raise ValidationError('Поле не может быть пустым.')


class Ingredient(models.Model):
    """Ingridient model"""

    name = models.CharField(
        max_length=MAX_LENGTH_200,
        verbose_name='Название ингредиента',
        help_text=(
            'Введите название ингредиента, '
            'поле обязательное для заполнения'
        ),
        blank=True,
        db_index=True
    )

    measurement_unit = models.CharField(
        max_length=MAX_LENGTH_200,
        verbose_name='Единица измерения для ингредиента',
        help_text=(
            'Введите единицу измерения для ингредиента, '
            'поле обязательное для заполнения'
        ),
        blank=True
    )

    class Meta:
        """Ingredient model settings."""

        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            )
        ]

        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        """String representation of the class"""

        return self.name


class Tag(models.Model):
    """Tag model"""

    name = models.CharField(
        max_length=MAX_LENGTH_200,
        verbose_name='Название тега',
        help_text=(
            'Введите тег для рецепта, '
            'поле обязательное для заполнения, '
            'поле должно быть уникальным'
        ),
        unique=True

    )

    color = models.CharField(
        validators=[hex_name_color_validator],
        max_length=MAX_LENGTH_7
    )

    slug = models.SlugField(
        validators=[
            RegexValidator
            (regex=r'^[\w.@+-]+$',
             message=(
                 'Неправильный формат поля'
                 'Поле может содержать только буквы,'
                 'цифры и следующие символы: @ . + -'
             ),
             code='invalid_field')
        ],
        max_length=MAX_LENGTH_200,
        verbose_name='Slug тега',
        help_text=(
            'Введите тег рецепта, '
            'поле обязательное для заполнения, '
            'поле должно быть уникальным'
        ),
        unique=True,
        db_index=True
    )

    class Meta:
        """User model settings."""

        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        """String representation of the class"""

        return self.name


class Recipe(models.Model):
    """Recipe model"""

    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text=(
            'Введите автора рецепта, '
            'поле обязательное для заполнения'
        ),
        blank=True
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='RecipeIngredients',
        verbose_name='Список ингредиентов',
        help_text=(
            'Введите ингредиенты, '
            'поле обязательное для заполнения'
        ),
        blank=False,
        db_index=True
    )

    tags = models.ManyToManyField(
        Tag,
        validators=[validate_non_empty],
        through='RecipeTag',
        related_name='RecipeTag',
        verbose_name='Список тегов',
        help_text=(
            'Введите тег, '
            'поле обязательное для заполнения'
        ),
        blank=False,
        db_index=True
    )

    image = models.ImageField(
        upload_to='foodgram/images/',
        null=False,
        default=None,
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text=(
            'Введите название рецепта, '
            'поле обязательное для заполнения'
        ),
        blank=True

    )

    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text=(
            'Введите описание рецепта,'
            'поле обязательное для заполнения'
        )
    )

    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text=(
            'Введите время приготовления рецепта в минутах,'
            'можно ввести только целое число, '
            'поле обязательное для заполнения'
        ),
        validators=[
            validators.MinValueValidator(
                MIN_VALUE_1,
                MIN_VALIDATOR_ERROR_MESSAGE
            ),
            validators.MaxValueValidator(
                MAX_VALUE_1440,
                MAX_VALIDATOR_ERROR_MESSAGE
            )
        ]
    )

    pub_date = models.DateField(
        auto_now=True,
    )

    class Meta:
        """User model settings."""

        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
    
    def clean(self):
        if not self.tags.all().exists():
            raise ValidationError('Нужно выбрать минимум один тег.')
        if not self.ingredients.all().exists():
            raise ValidationError('Нужно выбрать минимум один ингредиент.')
    
    def save(self, *args, **kwargs):
        if not self.tags.exists() or not self.ingredients.exists():
            raise ValidationError('Необходимо выбрать минимум один тег и один ингредиент.')
        
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """String representation of the class"""

        return self.name


class RecipeIngredient(models.Model):
    """Model for linking models Recipe and Ingridient"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        db_index=True
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        db_index=True
    )

    amount = models.IntegerField(
        verbose_name='Количество ингредиента',
        help_text=(
            'Введите количество ингредиента,'
            'можно ввести только целое число, '
            'поле обязательное для заполнения'
        ),
        validators=[
            validators.MinValueValidator(
                MIN_VALUE_1,
                MIN_VALIDATOR_ERROR_MESSAGE
            ),
            validators.MaxValueValidator(
                MAX_VALUE_10000,
                MAX_VALIDATOR_AMOUNT_ERROR_MESSAGE
            )
        ]
    )

    class Meta:
        """RecipeIngredient model settings."""

        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self) -> str:
        """String representation of the class"""

        return f'Рецепт {self.recipe} с ингредиентом {self.ingredient}'


class RecipeTag(models.Model):
    """Model for linking models Recipe and Tag"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        db_index=True
    )

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        db_index=True
    )

    class Meta:
        """RecipeTag model settings."""

        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_recipe_tag'
            )
        ]

        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Тег рецептов'

    def __str__(self) -> str:
        """String representation of the class"""

        return f'Рецепт {self.recipe} с тегом {self.tag}'
