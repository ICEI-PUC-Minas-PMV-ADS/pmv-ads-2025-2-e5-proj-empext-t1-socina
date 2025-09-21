#!/usr/bin/env python
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "loja.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django. Certifique-se de que está instalado "
            "e que o ambiente virtual está ativado."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
