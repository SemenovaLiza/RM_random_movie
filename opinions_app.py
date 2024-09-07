from datetime import datetime
from random import randrange

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MY SECRET KEY'

db = SQLAlchemy(app)


class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


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


@app.route('/')
def index_view():
    quantity = Opinion.query.count()
    if not quantity:
        return 'There is no movies we can recommend to you yet'
    offset_value = randrange(quantity)
    opinion = Opinion.query.offset(offset_value).first()
    return render_template('opinion.html', opinion=opinion)


@app.route('/opinions/<int:id>')  
def opinion_view(id):  
    opinion = Opinion.query.get_or_404(id)  
    return render_template('opinion.html', opinion=opinion) 


@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    form = OpinionForm()
    if form.validate_on_submit():
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)


if __name__ == '__main__':
    app.run()