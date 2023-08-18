from foodgram.models import Tag


def save_tags_for_recipes(tags_data, recipe):
    """"Saving recipe tags"""

    for tag_id in tags_data:
        tag = Tag.objects.get(id=tag_id)
        recipe.tags.add(tag)
