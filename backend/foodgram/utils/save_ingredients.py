from foodgram.models import Ingredient, RecipeIngredient


def save_ingredients_for_resipe(ingredients_data, recipe):
    """Saving recipe ingredients"""

    for ingredient_data in ingredients_data:
        ingredient_id = ingredient_data.get('id')
        ingredient = Ingredient.objects.get(id=ingredient_id)
        ingredient_amount = ingredient_data.get('amount')
        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            amount=ingredient_amount
        )
