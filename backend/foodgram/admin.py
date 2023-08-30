from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from foodgram.models import (
    Ingredient,
    Recipe,
    RecipeTag,
    RecipeIngredient,
    Tag
)


class RecipeIngredientInline(admin.TabularInline):
    """
    RecipeIngredient inline class for displaying a field
    in the Recipe class in the admin
    """

    model = RecipeIngredient
    fk_name = 'recipe'
    extra = 1


class RecipeTagInline(admin.TabularInline):
    """
    RecipeTag inline class for displaying a field
    in the Recipe class in the admin
    """

    model = RecipeTag
    fk_name = 'recipe'
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    """Ingridient model settings in admin"""

    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = 'пусто'


class TagAdmin(admin.ModelAdmin):
    """Tag model settings in admin"""

    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = 'пусто'


class CustomRecipeForm(forms.ModelForm):
    """Set"""

    class Meta:
        """Set"""

        model = Recipe
        fields = (
            'pk',
            'author',
            'name',
            'display_ingredient',
            'display_tag',
            'image',
            'text',
            'cooking_time',
            'pub_date'
        )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data['tags'].exists() or not cleaned_data['ingredients'].exists():
            raise ValidationError('Необходимо выбрать минимум один тег и один ингредиент.')


class RecipeAdmin(admin.ModelAdmin):
    """Recipe model settings in admin"""

    form = CustomRecipeForm

    list_display = (
        'pk',
        'author',
        'name',
        'display_ingredient',
        'display_tag',
        'image',
        'text',
        'cooking_time',
        'pub_date'
    )

    def display_ingredient(self, obj):
        """
        Method for the Recipe model in the admin
        to display the recipe's ingredients
        """

        ingredients = obj.ingredients.all()
        return ', '.join([str(ingredient) for ingredient in ingredients])

    def display_tag(self, obj):
        """
        Method for the User model in the admin
        to display the resipe's tags
        """

        tags = obj.tags.all()
        return ', '.join([str(tag) for tag in tags])
    
    def save_model(self, request, obj, form, change):
        """
        Override user model save method,
        to properly hash the password before storing.
        """

        if not obj.ingredients and not obj.tags:
            raise ValidationError('Нужно выбрать минимум один тег и один ингредиент.')

        super().save_model(request, obj, form, change)
    
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        
        recipe = form.instance
        if not recipe.tags.exists() or not recipe.ingredients.exists():
            raise ValueError('Нужно выбрать минимум один тег и один ингредиент.')

    display_ingredient.short_description = 'Ингредиенты'
    display_tag.short_description = 'Теги'
    list_display_links = ('name',)
    search_fields = ('name', 'author', 'pub_date')
    list_filter = ('name', 'pub_date')
    empty_value_display = 'пусто'
    inlines = [RecipeIngredientInline, RecipeTagInline]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
