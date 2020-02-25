from django.apps import AppConfig
from importlib import import_module
from glob import glob


class GbexAppConfig(AppConfig):
    name = 'GBEX_app'

    def ready(self):
        # import models
        model_files = glob("GBEX_app/models/*.py")
        model_files.remove("GBEX_app/models/__init__.py")
        model_modules = [import_module(x.replace("/", ".")[:-3]) for x in model_files]
