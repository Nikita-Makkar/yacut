from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

from .validators import validate_short_url


class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256)]
    )
    short = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16), Optional(), validate_short_url]
    )
    submit = SubmitField('Создать')
