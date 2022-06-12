from functools import cached_property

from django.db import models
from django.db.models import Max, Prefetch, Q
from django.utils import timezone, translation
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    PageChooserPanel,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Orderable, Page
from wagtail.images import get_image_model_string
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Rendition
from wagtail.snippets.models import register_snippet
from wagtailautocomplete.edit_handlers import AutocompletePanel

from home.fields import TranslatedField
from home.models.mixins import FixUrlMixin


class Event(FixUrlMixin, Page):
    event_id = models.IntegerField(unique=True, null=True, blank=True, default=None)
    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")
    short_overview_sk = models.CharField(
        max_length=255,
        blank=True,
    )
    short_overview_en = models.CharField(
        max_length=255,
        blank=True,
    )
    short_overview = TranslatedField("short_overview_sk", "short_overview_en")
    description_sk = RichTextField(blank=True)
    description_en = RichTextField(blank=True)
    description = TranslatedField("description_sk", "description_en")
    date_and_time = models.DateTimeField(
        default=timezone.now, verbose_name=_("date and time")
    )
    location = models.ForeignKey(
        "home.Location",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    video_url = models.URLField(
        null=True,
        blank=True,
        help_text=format_html(
            _("Supports Youtube, Vimeo and {}{}{}"),
            mark_safe(
                "<a href='https://github.com/wagtail/wagtail/blob/master/"
                "wagtail/embeds/oembed_providers.py' target='_blank'>"
            ),
            _("other websites"),
            mark_safe("</a>"),
        ),
    )
    ticket_url = models.URLField(
        null=True, blank=True, help_text="Defaultne používané pre jednorázový lístok"
    )
    ticket2_url = models.URLField(
        null=True, blank=True, help_text="Používané pre iný druh lístka."
    )
    buttons = StreamField(
        [
            (
                "button",
                blocks.StructBlock(
                    [
                        ("url", blocks.URLBlock()),
                        ("color", blocks.CharBlock(required=False)),
                        ("sk_text", blocks.CharBlock()),
                        ("en_text", blocks.CharBlock()),
                    ]
                ),
            ),
        ],
        blank=True,
        help_text="Tlačidlá len pre toto podujatie. Zobrazia sa vedla tlačidiel pre lístky.",
    )
    category = models.ForeignKey(
        "home.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    show_on_festivalpage = models.BooleanField(default=False)
    wordpress_url = models.CharField(max_length=255, unique=True, null=True, blank=True)
    related_festival = models.ForeignKey(
        "home.FestivalPage",
        on_delete=models.PROTECT,
        related_name="+",
    )

    content_panels_sk = Page.content_panels + [
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
                FieldPanel("short_overview_sk"),
                FieldPanel("description_sk"),
                FieldPanel("video_url"),
                FieldPanel("ticket_url"),
                FieldPanel("ticket2_url"),
                StreamFieldPanel("buttons"),
            ],
            heading=_("description"),
        ),
        InlinePanel("speaker_connections", heading="speakers"),
        InlinePanel("host_connections", heading="hosts"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
        MultiFieldPanel(
            [FieldPanel("short_overview_en"), FieldPanel("description_en")],
            heading=_("description"),
        ),
    ]
    promote_panels = Page.promote_panels + [
        FieldPanel("show_on_festivalpage"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )

    parent_page_types = ["home.EventIndexPage"]
    subpage_types = []

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")

    def get_url_parts(self, request=None):
        """Insert PK of object to url"""
        site_id, root_url, page_path = super().get_url_parts(request)
        page_path = page_path.split("/")
        page_path.insert(-2, str(self.event_id))
        return site_id, root_url, "/".join(page_path)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["today"] = timezone.now().date()
        return context

    def save(self, *args, **kwargs):
        if self.event_id is None:
            last_event_id = (
                Event.objects.aggregate(Max("event_id"))["event_id__max"] or 0
            )
            self.event_id = last_event_id + 1
        return super().save(*args, **kwargs)

    @cached_property
    def speakers_limited(self):
        connections = list(
            filter(lambda c: c.speaker is not None, self.speaker_connections.all())
        )
        return {
            "under_limit": [c.speaker.title for c in connections[:3]],
            "over_limit_count": len(connections[3:]),
            "over_limit_names": ", ".join(c.speaker.title for c in connections[3:]),
        }

    def delete(self, *args, **kwargs):
        self.unpublish(user=kwargs.get("user"))


class SpeakerConnection(Orderable):
    event = ParentalKey(
        "home.Event", on_delete=models.CASCADE, related_name="speaker_connections"
    )
    speaker = models.ForeignKey(
        "home.Speaker",
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name="speaker_connections",
    )

    panels = [AutocompletePanel("speaker")]


class HostConnection(Orderable):
    event = ParentalKey(
        "home.Event", on_delete=models.CASCADE, related_name="host_connections"
    )
    speaker = models.ForeignKey(
        "home.Speaker",
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        related_name="host_connections",
    )

    panels = [AutocompletePanel("speaker")]


class Speaker(FixUrlMixin, Page):
    speaker_id = models.IntegerField(unique=True, null=True, blank=True, default=None)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64)
    description_sk = RichTextField(blank=True)
    description_en = RichTextField(blank=True)
    description = TranslatedField("description_sk", "description_en")
    wordpress_url = models.CharField(max_length=255, unique=True, null=True, blank=True)
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        verbose_name = _("speaker")
        verbose_name_plural = _("speakers")

    parent_page_types = ["home.SpeakerIndexPage"]
    content_panels_sk = Page.content_panels + [
        FieldRowPanel([FieldPanel("first_name"), FieldPanel("last_name")]),
        ImageChooserPanel("photo"),
        FieldPanel("description_sk"),
    ]
    content_panels_en = Page.content_panels + [
        FieldPanel("description_en"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )

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
        from home.models.pages import ancestor_festival

        context = super().get_context(request, *args, **kwargs)
        context["events"] = (
            Event.objects.filter(
                Q(speaker_connections__speaker=self) | Q(host_connections__speaker=self)
            )
            .distinct()
            .live()
            .prefetch_related(
                Prefetch(
                    "icon__renditions",
                    queryset=Rendition.objects.filter(filter_spec="fill-65x65"),
                )
            )
        )
        return context

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def delete(self, *args, **kwargs):
        self.unpublish(user=kwargs.get("user"))


class HeroImage(Orderable):
    page = ParentalKey(
        "home.FestivalPage", on_delete=models.CASCADE, related_name="hero_images"
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
        "home.FestivalPage", on_delete=models.CASCADE, related_name="video_invites"
    )
    url = models.URLField()

    panels = [
        FieldPanel("url"),
    ]


class LocationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("title_sk")


@register_snippet
class Location(models.Model):
    title_sk = models.CharField(default="", max_length=255)
    title_en = models.CharField(default="", max_length=255)
    url_to_map = models.URLField(
        verbose_name=_("URL to map"),
        help_text=_("URL to Google Maps or similar service"),
    )

    title = TranslatedField("title_sk", "title_en")
    panels = [FieldPanel("title_sk"), FieldPanel("title_en"), FieldPanel("url_to_map")]
    autocomplete_search_field = "title_sk"

    objects = LocationManager()

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    def __str__(self):
        return self.title_sk

    def autocomplete_label(self):
        return self.title_sk


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("title_sk")


@register_snippet
class Category(models.Model):
    title_sk = models.CharField(max_length=30)
    title_en = models.CharField(max_length=30)
    color = models.CharField(max_length=20)

    title = TranslatedField("title_sk", "title_en")
    panels = [FieldPanel("title_sk"), FieldPanel("title_en"), FieldPanel("color")]
    autocomplete_search_field = "title_sk"

    objects = CategoryManager()

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.title_sk

    def autocomplete_label(self):
        return self.title_sk


class PartnerBlock(blocks.StructBlock):
    logo = ImageChooserBlock()
    url = blocks.URLBlock()

    class Meta:
        template = "home/blocks/partner.html"


class PartnerSectionBlock(blocks.StructBlock):
    title_sk = blocks.CharBlock()
    title_en = blocks.CharBlock()
    title = TranslatedField("title_sk", "title_en")
    partners = blocks.ListBlock(PartnerBlock)

    class Meta:
        template = "home/blocks/partner_section.html"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        if translation.get_language() == "en":
            context["translated_title"] = value["title_en"]
        else:
            context["translated_title"] = value["title_sk"]
        return context


class OpenGraphImage(models.Model):
    page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="open_graph_image",
    )
    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
    )
    lang_code = models.CharField(max_length=2, default="sk")

    class Meta:
        unique_together = ["page", "image", "lang_code"]
