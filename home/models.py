from django.db import models
from django.utils import timezone
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.fields import RichTextField

from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel


class HomePage(Page):
    hero_text = RichTextField(blank=True)
    video_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('hero_text', classname='full'),
        InlinePanel('hero_images', label='Hero images'),
        FieldPanel('video_text', classname='full'),
        InlinePanel('video_invites'),
        InlinePanel('partners'),
    ]


class HeroImage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='hero_images')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]


class VideoInvite(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='video_invites')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]


class Partner(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='partners')
    url = models.URLField()
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        ImageChooserPanel('logo'),
        FieldPanel('url'),
    ]


@register_setting
class HeaderSettings(BaseSetting):
    logo = models.FileField(null=True)
    title = RichTextField(default='Bratislavské Hanusove dni')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    place = models.CharField(max_length=50, default='Malá scéna STU')

    content_panels = Page.content_panels + [
        ImageChooserPanel('logo'),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
    ]
