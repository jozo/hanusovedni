from itertools import chain

from django import template
from django.utils.translation import get_language, to_locale

register = template.Library()


@register.simple_tag
def current_locale():
    return to_locale(get_language())


@register.filter
def prefix_festival(value, request):
    return "/".join(chain(request.path.split("/")[:3], value.split("/")[2:]))
