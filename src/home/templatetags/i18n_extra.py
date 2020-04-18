from django import template
from django.utils.translation import get_language, to_locale

register = template.Library()


@register.simple_tag
def current_locale():
    return to_locale(get_language())


@register.filter
def localize_url(value):
    if value and not value.startswith("http"):
        locale = to_locale(get_language())
        if value.startswith("/"):
            return f"/{locale}{value}"
        else:
            return f"/{locale}/{value}"
    return value
