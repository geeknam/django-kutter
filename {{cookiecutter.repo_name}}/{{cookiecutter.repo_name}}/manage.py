#!/usr/bin/env python
import os
import sys
import logging

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{cookiecutter.repo_name}}.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

    APPS_ROOT = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(APPS_ROOT, 'apps'))

    from configurations.management import execute_from_command_line
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        logging.disable(logging.CRITICAL)
    execute_from_command_line(sys.argv)
