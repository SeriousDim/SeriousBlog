import os
import click

# ВНИМАНИЕ! Для работы нужно установить переменную FLASK_APP=main.py!

def register(app):
    @app.cli.group()
    def translate():
        """I18n and L10n commands flask-babel."""
        pass

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o trns.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel init -i trns.pot -d app/translations -l '+lang):
            raise RuntimeError('init command failed')
        os.remove('trns.pot')

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o trns.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i trns.pot -d app/translations'):
            raise RuntimeError('update command failed')
        os.remove('trns.pot')

    @translate.command()
    def compile():
        """Compile all languages"""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile command failed')