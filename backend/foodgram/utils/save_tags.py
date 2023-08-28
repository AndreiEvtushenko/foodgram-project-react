from foodgram.models import RecipeTag


def save_tags_for_recipe(tags_data, recipe):
    """"Saving recipe tags"""

    recipe_tags_to_create = []

    for tag_id in tags_data:
        recipe_tags_to_create.append(RecipeTag(recipe=recipe, tag_id=tag_id))

    RecipeTag.objects.bulk_create(recipe_tags_to_create)
