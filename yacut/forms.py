from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class URLForm(FlaskForm):
    original = StringField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256)]
    )
    short = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')
