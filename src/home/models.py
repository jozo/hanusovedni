import itertools
import re
from collections import defaultdict
from functools import cached_property

from django.db import models
from django.db.models import Max
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.shortcuts import redirect
from django.utils import timezone, translation
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
    PageChooserPanel,
    StreamFieldPanel,
    TabbedInterface,
    ObjectList,
)
from wagtail.contrib.frontend_cache.utils import PurgeBatch
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
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
    # TODO move this to settings
    return FestivalPage.objects.get(slug="bhd-online")


class TranslatedField:
    def __init__(self, sk_field, en_field):
        self.sk_field = sk_field
        self.en_field = en_field

    def __get__(self, instance, owner):
        if translation.get_language() == "en":
            field = getattr(instance, self.en_field)
            if field:
                return field
        return getattr(instance, self.sk_field)


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
    formatted_title_sk = RichTextField(default="", verbose_name=_("titulok"))
    formatted_title_en = RichTextField(default="", verbose_name=_("titulok"))
    formatted_title = TranslatedField("formatted_title_sk", "formatted_title_en")
    logo = models.FileField(null=True, blank=True)
    start_date = models.DateField(
        default=timezone.now, verbose_name=_("začiatok festivalu")
    )
    end_date = models.DateField(
        default=timezone.now, verbose_name=_("koniec festivalu")
    )
    place = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_("miesto")
    )
    hero_text_sk = RichTextField(blank=True)
    hero_text_en = RichTextField(blank=True)
    hero_text = TranslatedField("hero_text_sk", "hero_text_en")
    hero_buttons_sk = StreamField(
        [
            (
                "hero_buttons",
                blocks.StructBlock(
                    [("title", blocks.CharBlock()), ("link", blocks.CharBlock())]
                ),
            ),
        ],
        null=True,
        blank=True,
        help_text=_("Len prvé 2 tlacidla budú použité"),
    )
    hero_buttons_en = StreamField(
        [
            (
                "hero_buttons",
                blocks.StructBlock(
                    [("title", blocks.CharBlock()), ("link", blocks.CharBlock())]
                ),
            ),
        ],
        null=True,
        blank=True,
        help_text=_("Len prvé 2 tlacidla budú použité"),
    )
    hero_buttons = TranslatedField("hero_buttons_sk", "hero_buttons_en")
    video_text_sk = RichTextField(blank=True)
    video_text_en = RichTextField(blank=True)
    video_text = TranslatedField("video_text_sk", "video_text_en")
    headline_sk = StreamField(
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
    headline_en = StreamField(
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
    headline = TranslatedField("headline_sk", "headline_en")

    content_panels_sk = [
        FieldPanel("formatted_title_sk"),
        FieldPanel("logo"),
        FieldRowPanel([FieldPanel("start_date"), FieldPanel("end_date")]),
        FieldPanel("place"),
        FieldPanel("hero_text_sk", classname="full"),
        InlinePanel("hero_images", label="Hero images"),
        StreamFieldPanel("hero_buttons_sk"),
        FieldPanel("video_text_sk", classname="full"),
        InlinePanel("video_invites"),
        StreamFieldPanel("headline_sk"),
        InlinePanel("partners", label=_("partneri")),
        InlinePanel("media_partners", label=_("mediálni partneri")),
    ]
    content_panels_en = [
        FieldPanel("formatted_title_en"),
        FieldPanel("hero_text_en", classname="full"),
        StreamFieldPanel("hero_buttons_en"),
        FieldPanel("video_text_en", classname="full"),
        StreamFieldPanel("headline_en"),
    ]
    promote_panels = Page.promote_panels + [InlinePanel("menu_items", label=_("Menu"))]
    subpage_types = [
        "home.ProgramIndexPage",
        "home.CrowdfundingPage",
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )

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

    def get_template(self, request, *args, **kwargs):
        if self.slug == "bhd-online":
            return "home/festival_page_online.html"
        return super().get_template(request, *args, **kwargs)


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
    title_sk = models.CharField(max_length=32)
    title_en = models.CharField(max_length=32)
    title = TranslatedField("title_sk", "title_en")
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
        context["speakers_by_year"] = self.get_speakers_by_year()
        # disable defaultdict because Django Template can't work with it
        context["speakers_by_year"].default_factory = None
        return context

    def get_speakers_by_year(self):
        speakers_by_year = defaultdict(dict)
        min_year = (
            Event.objects.live()
            .only("date_and_time")
            .earliest("date_and_time")
            .date_and_time.year
        )
        max_year = (
            Event.objects.live()
            .only("date_and_time")
            .latest("date_and_time")
            .date_and_time.year
        )

        festivals = FestivalPage.objects.live().all()

        for year in range(max_year, min_year - 1, -1):
            for festival in festivals:
                speakers = (
                    Speaker.objects.live()
                    .filter(
                        events__related_festival=festival,
                        events__date_and_time__year=year,
                    )
                    .select_related("photo")
                    .order_by("last_name")
                    .distinct()
                )
                if speakers.exists():
                    speakers_by_year[year][festival] = speakers.all()

        return speakers_by_year


class Speaker(Page):
    speaker_id = models.IntegerField(unique=True, null=True, blank=True, default=None)
    first_name = models.CharField(max_length=64, verbose_name=_("meno"), blank=True)
    last_name = models.CharField(max_length=64, verbose_name=_("priezvisko"))
    description_sk = RichTextField(blank=True, verbose_name=_("popis"))
    description_en = RichTextField(blank=True)
    description = TranslatedField("description_sk", "description_en")
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
            .only(
                "category",
                "location",
                "icon",
                "title",
                "date_and_time",
                "event_id",
                "url_path",
            )
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
            .select_related("category", "location", "icon")
            .order_by("date_and_time")
        )
        # TODO use iterator
        context["grouped_events"] = {
            k: list(v)
            for k, v in itertools.groupby(events, lambda e: e.date_and_time.date())
        }
        if self.get_parent().slug == "bhd-online":
            context["message_empty"] = "Program prvého BHD ONLINE už čoskoro…"
        return context


class Event(Page):
    event_id = models.IntegerField(unique=True, null=True, blank=True, default=None)
    short_overview_sk = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("krátky popis"),
        help_text=_("Zobrazuje sa na stránke s programom"),
    )
    short_overview_en = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("krátky popis"),
        help_text=_("Zobrazuje sa na stránke s programom"),
    )
    short_overview = TranslatedField("short_overview_sk", "short_overview_en")
    description_sk = RichTextField(blank=True, verbose_name=_("popis"))
    description_en = RichTextField(blank=True, verbose_name=_("popis"))
    description = TranslatedField("description_sk", "description_en")
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
            ],
            heading=_("Popis"),
        ),
        AutocompletePanel("speakers"),
    ]
    content_panels_en = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("short_overview_en"),
                FieldPanel("description_en"),
            ],
            heading=_("Popis"),
        ),
        AutocompletePanel("speakers"),
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
        speakers = list(self.speakers.all().only("title"))
        return {
            "under_limit": speakers[:3],
            "over_limit_count": len(speakers[3:]),
            "over_limit_names": ", ".join(s.title for s in speakers[3:]),
        }


@register_snippet
class Location(models.Model):
    title_sk = models.CharField(default="", max_length=255, verbose_name=_("názov"))
    title_en = models.CharField(default="", max_length=255, verbose_name=_("názov"))
    url_to_map = models.URLField(
        verbose_name=_("URL k mape"),
        help_text=_("URL adresa na Google Mapy alebo obdobnú službu"),
    )

    panels = [FieldPanel("title_sk"), FieldPanel("title_en"), FieldPanel("url_to_map")]

    class Meta:
        verbose_name = _("poloha")
        verbose_name_plural = _("polohy")

    def __str__(self):
        return " ".join(replace_tags_with_space(self.title).split())


@register_snippet
class Category(models.Model):
    title_sk = models.CharField(max_length=30)
    title_en = models.CharField(max_length=30)
    color = models.CharField(max_length=20, verbose_name=_("farba"))

    panels = [FieldPanel("title_sk"), FieldPanel("title_en"), FieldPanel("color")]

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
    left_text_sk = RichTextField()
    left_text_en = RichTextField()
    left_text = TranslatedField("left_text_sk", "left_text_en")
    right_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="r_img+",
    )
    right_text_sk = RichTextField()
    right_text_en = RichTextField()
    right_text = TranslatedField("right_text_sk", "right_text_en")

    class Meta:
        verbose_name = _("kontakt")

    content_panels_sk = Page.content_panels + [
        ImageChooserPanel("left_image"),
        FieldPanel("left_text_sk", classname="full"),
        ImageChooserPanel("right_image"),
        FieldPanel("right_text_sk", classname="full"),
    ]
    content_panels_en = Page.content_panels + [
        FieldPanel("left_text_en", classname="full"),
        FieldPanel("right_text_en", classname="full"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = last_festival()
        return context


class AboutFestivalPage(Page):
    body_sk = StreamField(
        [
            ("heading", blocks.CharBlock(classname="title")),
            ("paragraph", blocks.RichTextBlock()),
        ]
    )
    body_en = StreamField(
        [
            ("heading", blocks.CharBlock(classname="title")),
            ("paragraph", blocks.RichTextBlock()),
        ]
    )
    body = TranslatedField("body_sk", "body_en")

    class Meta:
        verbose_name = _("o festivale")

    content_panels_sk = Page.content_panels + [
        StreamFieldPanel("body_sk"),
    ]
    content_panels_en = Page.content_panels + [
        StreamFieldPanel("body_en"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = last_festival()
        return context


class DonatePage(Page):
    body_sk = StreamField(
        [
            ("heading", blocks.CharBlock(classname="title")),
            ("paragraph", blocks.RichTextBlock()),
        ]
    )
    body_en = StreamField(
        [
            ("heading", blocks.CharBlock(classname="title")),
            ("paragraph", blocks.RichTextBlock()),
        ]
    )
    body = TranslatedField("body_sk", "body_en")

    class Meta:
        verbose_name = _("podpora")

    content_panels_sk = Page.content_panels + [
        StreamFieldPanel("body_sk"),
    ]
    content_panels_en = Page.content_panels + [
        StreamFieldPanel("body_en"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = last_festival()
        return context


class PartnersPage(Page):
    body_sk = StreamField(
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
    body_en = StreamField(
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
    body = TranslatedField("body_sk", "body_en")

    class Meta:
        verbose_name = _("partneri")

    content_panels_sk = Page.content_panels + [
        StreamFieldPanel("body_sk"),
    ]
    content_panels_en = Page.content_panels + [
        StreamFieldPanel("body_en"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = last_festival()
        return context


class CrowdfundingPage(Page):
    body_sk = StreamField([("text", blocks.TextBlock())])
    body_en = StreamField([("text", blocks.TextBlock())])
    body = TranslatedField("body_sk", "body_en")

    content_panels_sk = Page.content_panels + [
        StreamFieldPanel("body_sk"),
    ]
    content_panels_en = Page.content_panels + [
        StreamFieldPanel("body_en"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["festival"] = FestivalPage.objects.get(pk=self.get_parent().pk)
        return context


def purge_cache_for_indexes(blog_page):
    pages = set()
    batch = PurgeBatch()
    for event_index in EventIndexPage.objects.live():
        pages.add(event_index)
    for program_index in ProgramIndexPage.objects.live():
        pages.add(program_index)
    for festival_page in FestivalPage.objects.live():
        pages.add(festival_page)
    pages.add(HomePage.objects.get())
    pages.add(blog_page)
    batch.add_pages(pages)
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
