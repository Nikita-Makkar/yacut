import re

from wtforms.validators import ValidationError


def validate_short_url(form, field):
    short_url = field.data
    if short_url:
        if len(short_url) > 16:
            raise ValidationError('Короткая ссылка не может быть длиннее 16 символов.')

        if not re.match(r'^[A-Za-z0-9]+$', short_url):
            raise ValidationError('Короткая ссылка может содержать только латинские буквы и цифры.')
