from django.contrib import admin
from reversion_compare.admin import CompareVersionAdmin
from django.apps import apps
from glob import glob
from importlib import import_module

model_files = glob("GBEX_app/models/*.py")
model_files.remove("GBEX_app/models/__init__.py")
model_modules = [import_module(x.replace("/", ".")[:-3]) for x in model_files]


for model in apps.get_app_config('GBEX_app').get_models():
	modeladmin = type(f"{model.__name__}Admin", (CompareVersionAdmin,), {})
	admin.site.register(model, modeladmin)
