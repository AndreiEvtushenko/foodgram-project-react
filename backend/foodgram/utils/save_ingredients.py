from foodgram.models import Ingredient, RecipeIngredient


def save_ingredients_for_recipe(ingredients_data, recipe):
    """Saving recipe ingredients"""

    recipe_ingredients_to_create = []

    for ingredient_data in ingredients_data:
        # ingredient_id = ingredient_data.get('id')
        # ingredient = Ingredient.objects.get(id=ingredient_id)
        # ingredient_amount = ingredient_data.get('amount')

        recipe_ingredients_to_create.append(
            RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient_data.get('id'),
                amount=ingredient_data.get('amount')
            )
        )

    RecipeIngredient.objects.bulk_create(recipe_ingredients_to_create)
