from django.contrib import admin

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


class RecipeAdmin(admin.ModelAdmin):
    """Recipe model settings in admin"""

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
