import psycopg2
from flask import current_app, g
import click

def get_db_conn():
    if 'db_conn' not in g:
        g.db_conn = psycopg2.connect(
            host=current_app.config['DB_HOST'],
            database=current_app.config['DB_NAME'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD']
        )
    return g.db_conn

def close_db_conn(e=None):
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()

def init_db():
    db_conn = get_db_conn()
    with current_app.open_resource('schema.sql') as f:
        db_conn.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db_conn)
    app.cli.add_command(init_db_command)

