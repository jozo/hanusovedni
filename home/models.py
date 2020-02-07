import itertools
from django.db import models
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.html import format_html, strip_tags
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

# TODO - gettext vs ugettext_lazy
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtailautocomplete.edit_handlers import AutocompletePanel


class HomePage(Page):
    hero_text = RichTextField(blank=True)
    video_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("hero_text", classname="full"),
        InlinePanel("hero_images", label="Hero images"),
        FieldPanel("video_text", classname="full"),
        InlinePanel("video_invites"),
        InlinePanel("partners"),
    ]
    subpage_types = [
        "home.EventIndexPage",
        "home.SpeakerIndexPage",
        "home.ProgramIndexPage",
    ]

    @property
    def events(self):
        return Event.objects.all()


class HeroImage(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="hero_images")
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel("name"),
        FieldPanel("url"),
    ]


class VideoInvite(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="video_invites")
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel("name"),
        FieldPanel("url"),
    ]


class Partner(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="partners")
    url = models.URLField()
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        ImageChooserPanel("logo"),
        FieldPanel("url"),
    ]


class SpeakerIndexPage(RoutablePageMixin, Page):
    class Meta:
        verbose_name = _("rečníci")

    @route(r"^(\d+)/(\w+)")
    def speaker_with_id_in_url(self, request, speaker_id, slug):
        speaker = Speaker.objects.get(pk=speaker_id)
        if slug == speaker.slug:
            return speaker.serve(request)
        return redirect(speaker.get_url(request))


class Speaker(Page):
    first_name = models.CharField(max_length=30, verbose_name=_("meno"))
    last_name = models.CharField(max_length=30, verbose_name=_("priezvisko"))
    description = RichTextField(blank=True, verbose_name=_("popis"))
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("fotka"),
    )

    content_panels = [
        FieldRowPanel([FieldPanel("first_name"), FieldPanel("last_name")]),
        ImageChooserPanel("photo"),
        FieldPanel("description"),
    ]
    parent_page_types = ["home.SpeakerIndexPage"]

    def get_url_parts(self, request=None):
        """Insert PK of object to url"""
        site_id, root_url, page_path = super().get_url_parts(request)
        page_path = page_path.split("/")
        page_path.insert(-2, str(self.pk))
        return site_id, root_url, "/".join(page_path)

    def save(self, *args, **kwargs):
        self.draft_title = f"{self.first_name} {self.last_name}"
        self.title = self.draft_title
        if "updated_fields" in kwargs:
            kwargs["updated_fields"].append("title")
        return super().save(*args, **kwargs)


class EventIndexPage(RoutablePageMixin, Page):
    """Archive of all events"""

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]
    subpage_types = ["home.Event"]

    class Meta:
        verbose_name = _("archív")

    @route(r"^(\d+)/(\w+)")
    def event_with_id_in_url(self, request, event_id, slug):
        event = Event.objects.get(pk=event_id)
        if slug == event.slug:
            return event.serve(request)
        return redirect(event.get_url(request))

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        events = Event.objects.live().order_by("date_and_time")
        # TODO use iterator
        context["grouped_events"] = {
            k: list(v)
            for k, v in itertools.groupby(events, lambda e: e.date_and_time.date())
        }
        return context


class ProgramIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]
    subpage_types = []

    class Meta:
        verbose_name = _("program")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        hs = HeaderSettings.objects.get()
        events = (
            Event.objects.live()
                .filter(date_and_time__gte=hs.start_date, date_and_time__lt=hs.end_date)
                .order_by("date_and_time")
        )
        # TODO use iterator
        context["grouped_events"] = {
            k: list(v)
            for k, v in itertools.groupby(events, lambda e: e.date_and_time.date())
        }
        return context


class Event(Page):
    short_overview = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("krátky popis"),
        help_text=_("Zobrazuje sa na stránke s programom"),
    )
    description = RichTextField(blank=True, verbose_name=_("popis"))
    date_and_time = models.DateTimeField(
        default=timezone.now, verbose_name=_("dátum a čas")
    )
    location = models.ForeignKey(
        "home.Location",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("poloha"),
    )
    video_url = models.URLField(
        null=True,
        blank=True,
        help_text=format_html(
            _("Podporuje Youtube, Vimeo a {}{}{}"),
            mark_safe(
                "<a href='https://github.com/wagtail/wagtail/blob/master/"
                "wagtail/embeds/oembed_providers.py' target='_blank'>"
            ),
            _("dalšie stránky"),
            mark_safe("</a>"),
        ),
    )
    category = models.ForeignKey(
        "home.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("kategória"),
    )
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("ikona"),
    )
    speakers = ParentalManyToManyField(
        "home.Speaker", blank=True, related_name="speakers", verbose_name=_("rečník")
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date_and_time"),
                AutocompletePanel("location"),
                FieldPanel("category"),
                ImageChooserPanel("icon"),
            ]
        ),
        MultiFieldPanel(
            [
                FieldPanel("short_overview"),
                FieldPanel("description"),
                FieldPanel("video_url"),
            ],
            heading=_("Popis"),
        ),
        AutocompletePanel("speakers"),
    ]

    parent_page_types = ["home.EventIndexPage"]
    subpage_types = []

    class Meta:
        verbose_name = _("podujatie")
        verbose_name_plural = _("podujatia")

    def get_url_parts(self, request=None):
        """Insert PK of object to url"""
        site_id, root_url, page_path = super().get_url_parts(request)
        page_path = page_path.split("/")
        page_path.insert(-2, str(self.pk))
        return site_id, root_url, "/".join(page_path)


@register_snippet
class Location(models.Model):
    title = RichTextField(blank=True, verbose_name=_("názov"))
    url_to_map = models.URLField(
        verbose_name=_("URL k mape"),
        help_text=_("URL adresa na Google Mapy alebo obdobnú službu"),
    )

    panels = [FieldPanel("title"), FieldPanel("url_to_map")]

    class Meta:
        verbose_name = _("poloha")
        verbose_name_plural = _("polohy")

    def __str__(self):
        return strip_tags(self.title)


@register_snippet
class Category(models.Model):
    title = models.CharField(max_length=30)
    color = models.CharField(max_length=20, verbose_name=_("farba"))

    panels = [FieldPanel("title"), FieldPanel("color")]

    class Meta:
        verbose_name = _("kategória")
        verbose_name_plural = _("kategórie")

    def __str__(self):
        return self.title


@register_setting
class HeaderSettings(BaseSetting):
    logo = models.FileField(null=True)
    title = RichTextField(default="Bratislavské Hanusove dni")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    place = models.CharField(max_length=50, default="Malá scéna STU")

    content_panels = Page.content_panels + [
        ImageChooserPanel("logo"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
    ]
