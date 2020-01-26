from django import forms
from django.db import models
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, FieldRowPanel, PageChooserPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.fields import RichTextField

from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route


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

    @property
    def events(self):
        return Event.objects.all()


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


class SpeakerIndexPage(RoutablePageMixin, Page):
    @route(r'^(\d+)/(\w+)')
    def speaker_with_id_in_url(self, request, speaker_id, slug):
        speaker = Speaker.objects.get(pk=speaker_id)
        if slug == speaker.slug:
            return speaker.serve(request)
        return redirect(speaker.get_url(request))


class Speaker(Page):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldRowPanel([
            FieldPanel('first_name'),
            FieldPanel('last_name'),
        ]),
        FieldPanel('description'),
    ]

    def get_url_parts(self, request=None):
        """Insert PK of object to url"""
        site_id, root_url, page_path = super().get_url_parts(request)
        page_path = page_path.split('/')
        page_path.insert(-2, str(self.pk))
        return site_id, root_url, '/'.join(page_path)


class EventIndexPage(RoutablePageMixin, Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full')
    ]

    @route(r'^(\d+)/(\w+)')
    def event_with_id_in_url(self, request, event_id, slug):
        event = Event.objects.get(pk=event_id)
        if slug == event.slug:
            return event.serve(request)
        return redirect(event.get_url(request))


class Event(Page):
    subtitle = models.CharField(max_length=100, blank=True)
    description = RichTextField(blank=True)
    date_and_time = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=30)
    speakers = ParentalManyToManyField('home.Speaker', blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('subtitle'),
            FieldPanel('date_and_time'),
            FieldPanel('location'),
        ]),
        FieldPanel('description'),
        FieldPanel('speakers'),
        # FieldPanel('speakers', widget=forms.CheckboxSelectMultiple),
        # PageChooserPanel('speakers', 'home.Speaker'),
    ]

    parent_page_types = ['home.EventIndexPage']
    subpage_types = []

    def get_url_parts(self, request=None):
        """Insert PK of object to url"""
        site_id, root_url, page_path = super().get_url_parts(request)
        page_path = page_path.split('/')
        page_path.insert(-2, str(self.pk))
        return site_id, root_url, '/'.join(page_path)


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
