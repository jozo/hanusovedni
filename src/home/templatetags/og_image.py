from django import template
from django.utils import translation

from home.models.data_models import OpenGraphImage

register = template.Library()


@register.simple_tag()
def get_existing_og_image(page):
    cur_language = translation.get_language()
    try:
        og_image = OpenGraphImage.objects.get(page=page, lang_code=cur_language)
        return og_image.image
    except OpenGraphImage.DoesNotExist:
        return None
