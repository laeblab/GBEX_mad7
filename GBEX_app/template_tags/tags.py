from django import template
from django.urls import reverse
from django.apps import apps
import random

register = template.Library()


@register.filter
def to_class_name(value):
    return value.__class__.__name__


@register.inclusion_tag('GBEX_app/links.html')
def links(selected_model):
    menus = {}
    selected_menu = ""
    for model in apps.get_app_config('GBEX_app').get_models():
        if hasattr(model, "GBEX_Page"):
            if model.__name__ == selected_model:
                selected_menu = model.menu_label
            menus[model.menu_label] = reverse(f"list_{model.__name__}")
    return {
        "menus": menus,
        "selected_menu": selected_menu,
    }


@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)
