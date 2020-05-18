import itertools
import logging
import re
from collections import defaultdict

from django.db import models
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.translation import gettext as _
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    ObjectList,
    PageChooserPanel,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Rendition

from home.fields import TranslatedField
from home.models import Event, PartnerSectionBlock, Speaker

# TODO - gettext vs ugettext_lazy


logger = logging.getLogger(__name__)


class HomePage(Page):
    subpage_types = [
        "home.EventIndexPage",
        "home.SpeakerIndexPage",
        "home.FestivalPage",
        "home.ContactPage",
        "home.AboutFestivalPage",
        "home.DonatePage",
        "home.PartnersPage",
        "home.StreamPage",
    ]

    @property
    def festivals(self):
        return FestivalPage.objects.live()


class FestivalPage(Page):
    formatted_title_sk = RichTextField(default="", verbose_name=_("title"))
    formatted_title_en = RichTextField(default="", verbose_name=_("title"))
    formatted_title = TranslatedField("formatted_title_sk", "formatted_title_en")
    logo = models.FileField(null=True, blank=True)
    start_date = models.DateField(
        default=timezone.now, verbose_name=_("festival beginning")
    )
    end_date = models.DateField(default=timezone.now, verbose_name=_("festival end"))
    place = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_("place")
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
    partner_sections = StreamField(
        [("partner_section", PartnerSectionBlock())], blank=True
    )

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
    ]
    content_panels_en = [
        FieldPanel("formatted_title_en"),
        FieldPanel("hero_text_en", classname="full"),
        StreamFieldPanel("hero_buttons_en"),
        FieldPanel("video_text_en", classname="full"),
        StreamFieldPanel("headline_en"),
    ]
    promote_panels = Page.promote_panels + [
        InlinePanel("menu_items", label=_("menu")),
        StreamFieldPanel("partner_sections"),
    ]
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
                date_and_time__date__gte=self.start_date,
                date_and_time__date__lte=self.end_date,
                show_on_festivalpage=True,
            )
            .order_by("date_and_time")
        )

    def save(self, *args, **kwargs):
        self.draft_title = " ".join(
            replace_tags_with_space(self.formatted_title_sk).split()
        )
        self.title = self.draft_title
        if "updated_fields" in kwargs:
            kwargs["updated_fields"].append("title")
        return super().save(*args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = self
        return context


class SpeakerIndexPage(RoutablePageMixin, Page):
    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")

    content_panels_sk = Page.content_panels
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )

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
                        speaker_connections__event__related_festival=festival,
                        speaker_connections__event__date_and_time__year=year,
                    )
                    .select_related("photo")
                    .order_by("last_name")
                    .distinct()
                )
                if speakers.exists():
                    speakers_by_year[year][festival] = speakers.all()

        return speakers_by_year


class ArchiveQueryset(models.QuerySet):
    def events(self):
        return (
            Event.objects.live()
            .order_by("-date_and_time")
            .select_related("icon", "category", "location")
            .prefetch_related("host_connections__speaker")
            .prefetch_related(
                Prefetch(
                    "speaker_connections__speaker",
                    queryset=Speaker.objects.live().only("title"),
                )
            )
            .prefetch_related(
                Prefetch(
                    "icon__renditions",
                    queryset=Rendition.objects.filter(filter_spec="fill-65x65"),
                )
            )
            .only(
                "title",
                "title_en",
                "event_id",
                "url_path",
                "date_and_time",
                "location__title_sk",
                "location__title_en",
                "category__color",
                "category__title_sk",
                "category__title_en",
                "icon__title",
            )
        )

    def json(self):
        result = {"events": []}
        for event in self.events()[:10]:
            d = {
                "title": event.title,
                "url": event.url,
                "date_and_time": date_format(event.date_and_time, "j.n. — l — G:i").upper(),
                "location": event.location.title,
                "category": {
                    "title": event.category.title,
                    "color": event.category.color,
                },
            }
            if event.icon:
                d["icon"] = {
                    "title": event.icon.title,
                    "url": event.icon.renditions.all()[0].url,
                }
            else:
                d["icon"] = None
            result["events"].append(d)
        return result


class EventIndexPage(RoutablePageMixin, Page):
    """Archive of all events"""

    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]
    subpage_types = ["home.Event"]

    content_panels_sk = Page.content_panels
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )

    @route(r"^(\d+)/(.+)/")
    def event_with_id_in_url(self, request, event_id, slug):
        event = Event.objects.get(event_id=event_id)
        if slug == event.slug:
            return event.serve(request)
        return redirect(event.get_url(request))

    @route(r"^json/$")
    def json_index(self, request):
        return JsonResponse(ArchiveQueryset().json())

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = last_festival()
        context["events"] = ArchiveQueryset().events()
        # context["events_json"] = ArchiveQueryset().json()
        return context


class ProgramIndexPage(Page):
    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")

    content_panels_sk = Page.content_panels
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        parent_festival = FestivalPage.objects.get(pk=self.get_parent().pk)
        context["header_festival"] = parent_festival
        events = (
            Event.objects.live()
            .filter(
                date_and_time__date__gte=parent_festival.start_date,
                date_and_time__date__lte=parent_festival.end_date,
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


class ContactPage(Page):
    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")
    left_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="l_img+",
    )
    left_text_sk = RichTextField(blank=True, null=True)
    left_text_en = RichTextField(blank=True, null=True)
    left_text = TranslatedField("left_text_sk", "left_text_en")
    right_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="r_img+",
    )
    right_text_sk = RichTextField(blank=True, null=True)
    right_text_en = RichTextField(blank=True, null=True)
    right_text = TranslatedField("right_text_sk", "right_text_en")

    content_panels_sk = Page.content_panels + [
        ImageChooserPanel("left_image"),
        FieldPanel("left_text_sk", classname="full"),
        ImageChooserPanel("right_image"),
        FieldPanel("right_text_sk", classname="full"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
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
    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")
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

    content_panels_sk = Page.content_panels + [
        StreamFieldPanel("body_sk"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
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
    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")
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

    content_panels_sk = Page.content_panels + [
        StreamFieldPanel("body_sk"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
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
    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")
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

    content_panels_sk = Page.content_panels + [
        StreamFieldPanel("body_sk"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
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
    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")
    body_sk = StreamField([("text", blocks.TextBlock())])
    body_en = StreamField([("text", blocks.TextBlock())])
    body = TranslatedField("body_sk", "body_en")

    content_panels_sk = Page.content_panels + [
        StreamFieldPanel("body_sk"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
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


class StreamPage(Page):
    stream_url = models.URLField(blank=True)
    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")
    body_sk = RichTextField(blank=True)
    body_en = RichTextField(blank=True)
    body = TranslatedField("body_sk", "body_en")
    button_text_sk = models.CharField(max_length=100)
    button_text_en = models.CharField(max_length=100)
    button_text = TranslatedField("button_text_sk", "button_text_en")
    background = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL,
    )
    google_form_url = models.URLField(blank=True)
    donate_button_text_sk = models.CharField(max_length=100, null=True)
    donate_button_text_en = models.CharField(max_length=100, null=True)
    donate_button_text = TranslatedField(
        "donate_button_text_sk", "donate_button_text_en"
    )
    donate_button_action = models.ForeignKey(
        Page, on_delete=models.SET_NULL, null=True, related_name="stream_page_donate"
    )

    content_panels_sk = Page.content_panels + [
        FieldPanel("stream_url"),
        FieldPanel("body_sk"),
        FieldPanel("button_text_sk"),
        ImageChooserPanel("background"),
        FieldPanel("donate_button_text_sk"),
        PageChooserPanel("donate_button_action"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
        FieldPanel("body_en"),
        FieldPanel("button_text_en"),
        FieldPanel("donate_button_text_en"),
    ]
    settings_panels = Page.settings_panels + [
        FieldPanel("google_form_url"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(settings_panels, heading="Settings", classname="settings"),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["header_festival"] = last_festival()
        return context


def replace_tags_with_space(value):
    """Return the given HTML with spaces instead of tags."""
    return re.sub(r"</?\w+>", " ", str(value))


def last_festival():
    # TODO move this to settings
    return FestivalPage.objects.get(slug="bhd-online")
