import csv
import click

from . import app, db
from .models import Opinion


@app.cli.command('load_data')
def load_data_command():
    with open('opinions.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data_counter = 0
        for row in reader:
            opinion = Opinion(**row)
            db.session.add(opinion)
            db.session.commit()
            data_counter += 1

    click.echo(f'{data_counter} data was loaded')
