"""
Use this rather than `python manage.py runserver` to ensure that it uses the correct host and port.
"""

if __name__ == "__main__":
    import os

    os.environ["DJANGO_SETTINGS_MODULE"] = "django_example.settings"

    from django.conf import settings

    os.system(f"python manage.py runserver {settings.HOST}:{settings.PORT}")
