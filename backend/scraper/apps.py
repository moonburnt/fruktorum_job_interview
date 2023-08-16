from django.apps import AppConfig
from os import environ


class ScraperConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "scraper"

    def ready(self):
        if environ.get("RUN_MAIN"):
            from . import signals
