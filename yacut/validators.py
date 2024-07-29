import re

from wtforms.validators import ValidationError

from yacut.constants import (ERROR_CHARACTERS, ERROR_SHORT_ID_LENGTH,
                             SHORT_ID_PATTERN)


def validate_short_url(form, field):
    short_url = field.data
    if short_url:
        if len(short_url) > 16:
            raise ValidationError(
                ERROR_SHORT_ID_LENGTH
            )

        if not re.match(SHORT_ID_PATTERN, short_url):
            raise ValidationError(
                ERROR_CHARACTERS
            )
