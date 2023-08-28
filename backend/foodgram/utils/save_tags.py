from foodgram.models import RecipeTag, Tag


def save_tags_for_recipe(tags_data, recipe):
    """"Saving recipe tags"""

    recipe_tags_to_create = []

    for tag_id in tags_data:
        # tag = Tag.objects.get(id=tag_id)
        recipe_tags_to_create.append(RecipeTag(recipe=recipe, tag_id=tag_id))
        # recipe.tags.add(tag)

    RecipeTag.objects.bulk_create(recipe_tags_to_create)
