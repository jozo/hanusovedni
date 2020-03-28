from django import template
from django.utils.translation import get_language, to_locale

register = template.Library()


@register.simple_tag
def current_locale():
    return to_locale(get_language())
