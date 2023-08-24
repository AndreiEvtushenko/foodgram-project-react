from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

import webcolors


def password_slug_username_validation(value):
    """Password field validation according to the documentation"""

    password_validator = RegexValidator(
        regex=r'^[\w.@+-]+$',
        message=(
            'Неправильный формат поля. '
            'Поле может содержать только буквы, '
            'цифры и следующие символы: @ . + -'
        ),
        code='invalid_field'
    )

    password_validator(value)


def hex_name_color_validator(value):
    """Checking if the given hex code exists in the database"""

    try:
        webcolors.hex_to_name(value)
    except ValueError as error:
        raise ValidationError(
            'Цвета с таким кодом нет в базе данных.'
        ) from error
