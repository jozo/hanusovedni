import itertools
import re

from django.db import models
from django.db.models import Max
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

# TODO - gettext vs ugettext_lazy
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
    PageChooserPanel,
)
from wagtail.contrib.frontend_cache.utils import PurgeBatch
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.contrib.settings.models import BaseSetting
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.core.signals import page_published
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtailautocomplete.edit_handlers import AutocompletePanel


def replace_tags_with_space(value):
    """Return the given HTML with spaces instead of tags."""
    return re.sub(r"</?\w+>", " ", str(value))


def last_festival():
    return FestivalPage.objects.live().order_by("end_date").last()


class HomePage(Page):
    subpage_types = [
        "home.EventIndexPage",
        "home.SpeakerIndexPage",
        "home.FestivalPage",
        "home.ContactPage",
        "home.AboutFestivalPage",
        "home.DonatePage",
        "home.PartnersPage",
    ]

    @property
    def festivals(self):
        return FestivalPage.objects.live()


class FestivalPage(Page):
    formatted_title = RichTextField(default="", verbose_name=_("titulok"))
    logo = models.FileField(null=True, blank=True)
    start_date = models.DateField(
        default=timezone.now, verbose_name=_("začiatok festivalu")
    )
    end_date = models.DateField(
        default=timezone.now, verbose_name=_("koniec festivalu")
    )
    place = models.CharField(
        max_length=50, default="Malá scéna STU", verbose_name=_("miesto")
    )
    hero_text = RichTextField(blank=True)
    video_text = RichTextField(blank=True)
    headline = StreamField(
        [
            (
                "headliner",
                blocks.StructBlock(
                    [
                        ("name", blocks.CharBlock()),
                        ("photo", ImageChooserBlock()),
                        ("link", blocks.PageChooserBlock(page_type="home.Speaker")),
                        ("description", blocks.RichTextBlock()),
                    ]
                ),
            ),
        ],
        null=True,
        blank=True,
    )

    content_panels = [
        FieldPanel("formatted_title"),
        FieldPanel("logo"),
        FieldRowPanel([FieldPanel("start_date"), FieldPanel("end_date")]),
        FieldPanel("place"),
        FieldPanel("hero_text", classname="full"),
        InlinePanel("hero_images", label="Hero images"),
        FieldPanel("video_text", classname="full"),
        InlinePanel("video_invites"),
        StreamFieldPanel("headline"),
        InlinePanel("partners", label=_("partneri")),
        InlinePanel("media_partners", label=_("mediálni partneri")),
    ]
    promote_panels = Page.promote_panels + [InlinePanel("menu_items", label=_("Menu"))]
    subpage_types = [
        "home.ProgramIndexPage",
    ]

    @property
    def events(self):
        return (
            Event.objects.live()
            .filter(
                date_and_time__gte=self.start_date,
                date_and_time__lt=self.end_date,
                show_on_festivalpage=True,
            )
            .order_by("date_and_time")
        )

    def save(self, *args, **kwargs):
        self.draft_title = " ".join(
            replace_tags_with_space(self.formatted_title).split()
        )
        self.title = self.draft_title
        if "updated_fields" in kwargs:
            kwargs["updated_fields"].append("title")
        return super().save(*args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = self
        return context


class HeroImage(Orderable):
    page = ParentalKey(
        FestivalPage, on_delete=models.CASCADE, related_name="hero_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    url = models.URLField()

    panels = [
        ImageChooserPanel("image"),
        FieldPanel("url"),
    ]


class VideoInvite(Orderable):
    page = ParentalKey(
        FestivalPage, on_delete=models.CASCADE, related_name="video_invites"
    )
    url = models.URLField()

    panels = [
        FieldPanel("url"),
    ]


class Partner(Orderable):
    page = ParentalKey(FestivalPage, on_delete=models.CASCADE, related_name="partners")
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


class MediaPartner(Orderable):
    page = ParentalKey(
        FestivalPage, on_delete=models.CASCADE, related_name="media_partners"
    )
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


class MenuItem(Orderable):
    page = ParentalKey(
        FestivalPage, on_delete=models.CASCADE, related_name="menu_items"
    )
    title = models.CharField(max_length=32, verbose_name=_("titulok"))
    link = models.CharField(max_length=255)


class SpeakerIndexPage(RoutablePageMixin, Page):
    class Meta:
        verbose_name = _("rečníci")

    subpage_types = [
        "home.Speaker",
    ]

    @route(r"^(\d+)/(.+)/")
    def speaker_with_id_in_url(self, request, speaker_id, slug):
        speaker = Speaker.objects.get(speaker_id=speaker_id)
        if slug == speaker.slug:
            return speaker.serve(request)
        return redirect(speaker.get_url(request))

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = last_festival()
        context["speakers"] = (
            Speaker.objects.live().select_related("photo").order_by("last_name")
        )
        return context


class Speaker(Page):
    speaker_id = models.IntegerField(unique=True, null=True, blank=True, default=None)
    first_name = models.CharField(max_length=64, verbose_name=_("meno"), blank=True)
    last_name = models.CharField(max_length=64, verbose_name=_("priezvisko"))
    description = RichTextField(blank=True, verbose_name=_("popis"))
    wordpress_url = models.CharField(max_length=255, unique=True, null=True, blank=True)
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("fotka"),
    )

    class Meta:
        verbose_name = _("rečník")
        verbose_name_plural = _("rečníci")

    content_panels = Page.content_panels + [
        FieldRowPanel([FieldPanel("first_name"), FieldPanel("last_name")]),
        ImageChooserPanel("photo"),
        FieldPanel("description"),
    ]
    parent_page_types = ["home.SpeakerIndexPage"]

    def get_url_parts(self, request=None):
        """Insert PK of object to url"""
        site_id, root_url, page_path = super().get_url_parts(request)
        page_path = page_path.split("/")
        page_path.insert(-2, str(self.speaker_id))
        return site_id, root_url, "/".join(page_path)

    def save(self, *args, **kwargs):
        if self.speaker_id is None:
            last_speaker_id = (
                Speaker.objects.aggregate(Max("speaker_id"))["speaker_id__max"] or 0
            )
            self.speaker_id = last_speaker_id + 1
        self.draft_title = f"{self.first_name} {self.last_name}".strip()
        self.title = self.draft_title
        if "updated_fields" in kwargs:
            kwargs["updated_fields"].append("title")
        return super().save(*args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = last_festival()
        context["speaker"] = self
        return context


class EventIndexPage(RoutablePageMixin, Page):
    """Archive of all events"""

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]
    subpage_types = ["home.Event"]

    class Meta:
        verbose_name = _("archív")

    @route(r"^(\d+)/(.+)/")
    def event_with_id_in_url(self, request, event_id, slug):
        event = Event.objects.get(event_id=event_id)
        if slug == event.slug:
            return event.serve(request)
        return redirect(event.get_url(request))

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = last_festival()
        context["events"] = (
            Event.objects.live()
            .select_related("category", "location", "icon")
            .order_by("-date_and_time")
        )
        return context


class ProgramIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]
    subpage_types = []

    class Meta:
        verbose_name = _("program")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        parent_festival = FestivalPage.objects.get(pk=self.get_parent().pk)
        context["header_festival"] = parent_festival
        events = (
            Event.objects.live()
            .filter(
                date_and_time__gte=parent_festival.start_date,
                date_and_time__lt=parent_festival.end_date,
            )
            .order_by("date_and_time")
        )
        # TODO use iterator
        context["grouped_events"] = {
            k: list(v)
            for k, v in itertools.groupby(events, lambda e: e.date_and_time.date())
        }
        return context


class Event(Page):
    event_id = models.IntegerField(unique=True, null=True, blank=True, default=None)
    short_overview = models.CharField(
        max_length=255,
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
    ticket_url = models.URLField(null=True, blank=True, verbose_name=_("Lístok URL"))
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
        "home.Speaker", blank=True, related_name="events", verbose_name=_("rečník")
    )
    show_on_festivalpage = models.BooleanField(default=False)
    wordpress_url = models.CharField(max_length=255, unique=True, null=True, blank=True)
    related_festival = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("festival"),
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date_and_time"),
                AutocompletePanel("location"),
                FieldPanel("category"),
                PageChooserPanel("related_festival", "home.FestivalPage"),
                ImageChooserPanel("icon"),
            ]
        ),
        MultiFieldPanel(
            [
                FieldPanel("short_overview"),
                FieldPanel("description"),
                FieldPanel("video_url"),
                FieldPanel("ticket_url"),
            ],
            heading=_("Popis"),
        ),
        AutocompletePanel("speakers"),
    ]
    promote_panels = Page.promote_panels + [
        FieldPanel("show_on_festivalpage"),
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
        page_path.insert(-2, str(self.event_id))
        return site_id, root_url, "/".join(page_path)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = last_festival()
        return context

    def save(self, *args, **kwargs):
        if self.event_id is None:
            last_event_id = (
                Event.objects.aggregate(Max("event_id"))["event_id__max"] or 0
            )
            self.event_id = last_event_id + 1
        return super().save(*args, **kwargs)


@register_snippet
class Location(models.Model):
    title = models.CharField(default="", max_length=255, verbose_name=_("názov"))
    url_to_map = models.URLField(
        verbose_name=_("URL k mape"),
        help_text=_("URL adresa na Google Mapy alebo obdobnú službu"),
    )

    panels = [FieldPanel("title"), FieldPanel("url_to_map")]

    class Meta:
        verbose_name = _("poloha")
        verbose_name_plural = _("polohy")

    def __str__(self):
        return " ".join(replace_tags_with_space(self.title).split())


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


class ContactPage(Page):
    left_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="l_img+",
    )
    left_text = RichTextField()
    right_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="r_img+",
    )
    right_text = RichTextField()

    class Meta:
        verbose_name = _("kontakt")

    content_panels = Page.content_panels + [
        ImageChooserPanel("left_image"),
        FieldPanel("left_text", classname="full"),
        ImageChooserPanel("right_image"),
        FieldPanel("right_text", classname="full"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = last_festival()
        return context


class AboutFestivalPage(Page):
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="title")),
            ("paragraph", blocks.RichTextBlock()),
        ]
    )

    class Meta:
        verbose_name = _("o festivale")

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = last_festival()
        return context


class DonatePage(Page):
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="title")),
            ("paragraph", blocks.RichTextBlock()),
        ]
    )

    class Meta:
        verbose_name = _("podpora")

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = last_festival()
        return context


class PartnersPage(Page):
    body = StreamField(
        [
            (
                "partner",
                blocks.StructBlock(
                    [
                        ("logo", ImageChooserBlock()),
                        ("description", blocks.RichTextBlock()),
                    ]
                ),
            ),
        ]
    )

    class Meta:
        verbose_name = _("partneri")

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = last_festival()
        return context


def purge_cache_for_indexes(blog_page):
    batch = PurgeBatch()
    for event_index in EventIndexPage.objects.live():
        batch.add_page(event_index)
    for program_index in ProgramIndexPage.objects.live():
        batch.add_page(program_index)
    for festival_page in FestivalPage.objects.live():
        batch.add_page(festival_page)
    batch.add_page(HomePage.objects.get())
    batch.add_page(blog_page)
    batch.purge()


@receiver(page_published, sender=Event)
def event_published_handler(**kwargs):
    purge_cache_for_indexes(kwargs["instance"])


@receiver(pre_delete, sender=Event)
def event_deleted_handler(**kwargs):
    purge_cache_for_indexes(kwargs["instance"])


@receiver(page_published, sender=Speaker)
def speaker_published_handler(**kwargs):
    purge_cache_for_indexes(kwargs["instance"])


@receiver(pre_delete, sender=Speaker)
def speaker_deleted_handler(**kwargs):
    purge_cache_for_indexes(kwargs["instance"])


@receiver(page_published, sender=FestivalPage)
def festival_published_handler(**kwargs):
    purge_cache_for_indexes(kwargs["instance"])


@receiver(pre_delete, sender=FestivalPage)
def festival_deleted_handler(**kwargs):
    purge_cache_for_indexes(kwargs["instance"])
