from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class OpinionForm(FlaskForm):
    title = StringField(
        'Movie title',
        validators=[DataRequired(message='Required field'), Length(1, 128)]
    )
    text = TextAreaField(
        'Share your opinion about this movie',
        validators=[DataRequired('Required field')]
    )
    source = URLField(
        'Add a link on detailed movie review',
        validators=(Length(1, 256), Optional())
    )
    submit = SubmitField('Add')
