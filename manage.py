#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.core.management import execute_from_command_line
from waitress import serve


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


IS_HEROKU = "DYNO" in os.environ


if __name__ == '__main__':
    if IS_HEROKU:
        serve(
            execute_from_command_line(['manage.py', 'runserver']),
            host='0.0.0.0',
            port=8000
        )
    else:
        main()
