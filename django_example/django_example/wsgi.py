"""
WSGI config for django_example project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

import dtale
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_example.settings")

from django.conf import settings

main_app = get_wsgi_application()

dtale.app.initialize_process_props(settings.DTALE_HOST, settings.PORT, False)
dtale_app = dtale.app.build_app(settings.DTALE_URL, host=settings.DTALE_HOST)


def combined_app(environ, start_response):
    host = environ.get("HTTP_HOST", "").split(":")[0]
    if host == settings.DTALE_HOST:
        return dtale_app(environ, start_response)
    return main_app(environ, start_response)


application = combined_app
