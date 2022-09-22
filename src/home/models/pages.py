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
    TabbedInterface,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Rendition
from wagtail.snippets.blocks import SnippetChooserBlock

from home.fields import TranslatedField
from home.models import Event, PartnerSectionBlock, Speaker
from home.models.mixins import FixUrlMixin

# TODO - gettext vs ugettext_lazy

logger = logging.getLogger(__name__)


class HomePage(FixUrlMixin, Page):
    subpage_types = [
        "home.EventIndexPage",
        "home.SpeakerIndexPage",
        "home.FestivalPage",
        "home.ContactPage",
        "home.AboutFestivalPage",
        "home.DonatePage",
        "home.PartnersPage",
        "home.StreamPage",
        "home.StreamPageMojeKino",
        "home.PodcastPage",
        "home.GenericPage",
    ]

    @property
    def festivals(self):
        return FestivalPage.objects.live()


class FestivalPage(FixUrlMixin, Page):
    formatted_title_sk = RichTextField(
        default="",
        verbose_name=_("title"),
        help_text=_("Visible in header next to the logo"),
    )
    formatted_title_en = RichTextField(
        default="",
        verbose_name=_("title"),
        help_text=_("Visible in header next to the logo"),
    )
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
        use_json_field=True,
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
        use_json_field=True,
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
                        ("link", blocks.PageChooserBlock()),
                        ("description", blocks.RichTextBlock()),
                    ]
                ),
            ),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    headline_en = StreamField(
        [
            (
                "headliner",
                blocks.StructBlock(
                    [
                        ("name", blocks.CharBlock()),
                        ("photo", ImageChooserBlock()),
                        ("link", blocks.PageChooserBlock()),
                        ("description", blocks.RichTextBlock()),
                    ]
                ),
            ),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    headline = TranslatedField("headline_sk", "headline_en")
    partner_sections = StreamField(
        [("partner_section", PartnerSectionBlock())], blank=True, use_json_field=True,
    )

    content_panels_sk = [
        FieldPanel(
            "title",
            heading=_("Internal title"),
            help_text=_("Visible only in the admin"),
        ),
        FieldPanel("formatted_title_sk"),
        FieldPanel("logo"),
        FieldRowPanel([FieldPanel("start_date"), FieldPanel("end_date")]),
        FieldPanel("place"),
        FieldPanel("hero_text_sk", classname="full"),
        InlinePanel("hero_images", label="Hero images"),
        FieldPanel("hero_buttons_sk"),
        FieldPanel("video_text_sk", classname="full"),
        InlinePanel("video_invites"),
        FieldPanel("headline_sk"),
        FieldPanel("partner_sections"),
    ]
    content_panels_en = [
        FieldPanel("formatted_title_en"),
        FieldPanel("hero_text_en", classname="full"),
        FieldPanel("hero_buttons_en"),
        FieldPanel("video_text_en", classname="full"),
        FieldPanel("headline_en"),
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
        context["header_festival"] = self
        context["events"] = (
            ArchiveQueryset()
            .events()
            .filter(
                date_and_time__date__gte=self.start_date,
                date_and_time__date__lte=self.end_date,
                show_on_festivalpage=True,
            )
            .order_by("date_and_time")
        )

        return context


class SpeakerIndexPage(RoutablePageMixin, FixUrlMixin, Page):
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

    @route(r"^(\d+)/(.+)/")
    def speaker_with_id_in_url(self, request, speaker_id, slug):
        speaker = Speaker.objects.get(speaker_id=speaker_id)
        if slug == speaker.slug:
            return speaker.serve(request)
        return redirect(speaker.get_url(request))

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["speakers_by_year"] = self.get_speakers_by_year()
        # disable defaultdict because Django Template can't work with it
        context["speakers_by_year"].default_factory = None
        return context

    def get_speakers_by_year(self):
        speakers_by_year = defaultdict(dict)
        if not Event.objects.live():
            return speakers_by_year
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

        festivals = FestivalPage.objects.live().order_by("-start_date").all()

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
            .distinct()
            .order_by("-date_and_time")
            .select_related("icon", "category", "location", "related_festival")
            .prefetch_related("host_connections__speaker")
            .prefetch_related(
                Prefetch(
                    "speaker_connections__speaker",
                    queryset=Speaker.objects.live().distinct().only("title"),
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
                "video_url",
                "date_and_time",
                "location__title_sk",
                "location__title_en",
                "category__color",
                "category__title_sk",
                "category__title_en",
                "icon__title",
                "related_festival__slug",
            )
        )

    def json(self):
        result = {"events": []}
        for event in self.events():
            d = {
                "title": event.title,
                "url": f"{event.event_id}/{event.slug}",
                "dateAndTime": {
                    "iso": event.date_and_time.isoformat(),
                    "repr": date_format(event.date_and_time, "j.n.Y — l — G:i").upper(),
                },
                "location": event.location.title if event.location else "",
                "speakers": event.speakers_limited,
                "extendedInfo": {
                    "hasVideo": bool(event.video_url),
                    "category": {
                        "title": event.category.title,
                        "color": event.category.color,
                    },
                    "festival": event.related_festival.slug.replace("-", " ").upper(),
                },
            }
            if event.icon:
                d["extendedInfo"]["icon"] = {
                    "title": event.icon.title,
                    "url": event.icon.renditions.all()[0].url,
                }
            else:
                d["extendedInfo"]["icon"] = None
            result["events"].append(d)
        return result


class EventIndexPage(RoutablePageMixin, FixUrlMixin, Page):
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
        # context["events"] = ArchiveQueryset().events()
        return context


class ProgramIndexPage(FixUrlMixin, Page):
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
            ArchiveQueryset()
            .events()
            .filter(
                date_and_time__date__gte=parent_festival.start_date,
                date_and_time__date__lte=parent_festival.end_date,
            )
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


class ContactPage(FixUrlMixin, Page):
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
        FieldPanel("left_image"),
        FieldPanel("left_text_sk", classname="full"),
        FieldPanel("right_image"),
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
        return context


class AboutFestivalPage(FixUrlMixin, Page):
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
        ],
        use_json_field=True,
    )
    body_en = StreamField(
        [
            ("heading", blocks.CharBlock(classname="title")),
            ("paragraph", blocks.RichTextBlock()),
        ],
        use_json_field=True,
    )
    body = TranslatedField("body_sk", "body_en")

    content_panels_sk = Page.content_panels + [
        FieldPanel("body_sk"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
        FieldPanel("body_en"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )


class DonatePage(FixUrlMixin, Page):
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
        ],
        use_json_field=True,
    )
    body_en = StreamField(
        [
            ("heading", blocks.CharBlock(classname="title")),
            ("paragraph", blocks.RichTextBlock()),
        ],
        use_json_field=True,
    )
    body = TranslatedField("body_sk", "body_en")

    content_panels_sk = Page.content_panels + [
        FieldPanel("body_sk"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
        FieldPanel("body_en"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )


class PartnersPage(FixUrlMixin, Page):
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
        ],
        use_json_field=True,
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
        ],
        use_json_field=True,
    )
    body = TranslatedField("body_sk", "body_en")

    content_panels_sk = Page.content_panels + [
        FieldPanel("body_sk"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
        FieldPanel("body_en"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )


class CrowdfundingPage(FixUrlMixin, Page):
    class Meta:
        verbose_name = "crowdfunding - rocket"

    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")
    body_sk = StreamField([("text", blocks.TextBlock())], use_json_field=True)
    body_en = StreamField([("text", blocks.TextBlock())], use_json_field=True)
    body = TranslatedField("body_sk", "body_en")

    content_panels_sk = Page.content_panels + [
        FieldPanel("body_sk"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
        FieldPanel("body_en"),
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
        context["festival"] = ancestor_festival(self)
        return context


class CrowdfundingStarsPage(FixUrlMixin, Page):
    class Meta:
        verbose_name = "crowdfunding - stars"

    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")
    body_sk = StreamField([("text", blocks.TextBlock())], use_json_field=True)
    body_en = StreamField([("text", blocks.TextBlock())], use_json_field=True)
    body = TranslatedField("body_sk", "body_en")

    content_panels_sk = Page.content_panels + [
        FieldPanel("body_sk"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
        FieldPanel("body_en"),
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
        context["festival"] = ancestor_festival(self)
        return context


class CrowdfundingRocket2Page(FixUrlMixin, Page):
    class Meta:
        verbose_name = "crowdfunding - rocket 2"

    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    target_amount = models.IntegerField()
    title_translated = TranslatedField("title", "title_en")
    body_sk = StreamField([("text", blocks.TextBlock())], use_json_field=True)
    body_en = StreamField([("text", blocks.TextBlock())], use_json_field=True)
    body = TranslatedField("body_sk", "body_en")

    content_panels_sk = Page.content_panels + [
        FieldPanel("target_amount"),
        FieldPanel("body_sk"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
        FieldPanel("body_en"),
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
        context["festival"] = ancestor_festival(self)
        return context


class CrowdfundingCandlePage(CrowdfundingRocket2Page):
    class Meta:
        verbose_name = "crowdfunding - candle"

    feed_url = models.URLField(
        blank=True, help_text="URL from darujme.sk with donation amount"
    )

    content_panels_sk = Page.content_panels + [
        FieldPanel("target_amount"),
        FieldPanel("feed_url"),
        FieldPanel("body_sk"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
        FieldPanel("body_en"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )


class StreamPage(FixUrlMixin, Page):
    stream_url = models.URLField(blank=True)
    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=True,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")
    popup_email_body_sk = RichTextField(blank=True)
    popup_email_body_en = RichTextField(blank=True)
    popup_email_body = TranslatedField("popup_email_body_sk", "popup_email_body_en")
    popup_email_button_sk = models.CharField(max_length=100)
    popup_email_button_en = models.CharField(max_length=100)
    popup_email_button = TranslatedField(
        "popup_email_button_sk", "popup_email_button_en"
    )
    popup_donation_body_sk = RichTextField(blank=True)
    popup_donation_body_en = RichTextField(blank=True)
    popup_donation_body = TranslatedField(
        "popup_donation_body_sk", "popup_donation_body_en"
    )
    popup_donation_button_sk = models.CharField(max_length=100, default="")
    popup_donation_button_en = models.CharField(max_length=100, default="")
    popup_donation_button = TranslatedField(
        "popup_donation_button_sk", "popup_donation_button_en"
    )
    popup_donation_button_url = models.URLField(blank=True, default="")
    background = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
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
    slido_url = models.URLField(blank=True, verbose_name="Sli.do")

    content_panels_sk = Page.content_panels + [
        FieldPanel("stream_url"),
        FieldPanel("background"),
        FieldPanel("popup_donation_body_sk"),
        FieldPanel("popup_donation_button_sk"),
        FieldPanel("popup_donation_button_url"),
        FieldPanel("popup_email_body_sk"),
        FieldPanel("popup_email_button_sk"),
        FieldPanel("donate_button_text_sk"),
        PageChooserPanel("donate_button_action"),
        FieldPanel("slido_url"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
        FieldPanel("popup_email_body_en"),
        FieldPanel("popup_email_button_en"),
        FieldPanel("popup_donation_body_en"),
        FieldPanel("popup_donation_button_en"),
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


class StreamPageMojeKino(StreamPage):
    pass


class PodcastPage(FixUrlMixin, Page):
    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=False,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")
    description_sk = RichTextField(blank=True)
    description_en = RichTextField(blank=True)
    description = TranslatedField("description_sk", "description_en")
    episodes = StreamField(
        [
            (
                "episode",
                blocks.StructBlock(
                    [
                        ("number", blocks.IntegerBlock(min_value=1)),
                        ("title_sk", blocks.CharBlock()),
                        ("title_en", blocks.CharBlock()),
                        ("category", SnippetChooserBlock("home.Category")),
                        ("url_anchor", blocks.URLBlock()),
                        ("url_apple", blocks.URLBlock()),
                        ("url_spotify", blocks.URLBlock()),
                    ]
                ),
            ),
        ],
        use_json_field=True,
    )

    content_panels = [
        FieldPanel("title", classname="full title", heading="Title SK"),
        FieldPanel("title_en", classname="full title", heading="Title EN"),
        FieldPanel("description_sk", classname="full"),
        FieldPanel("description_en", classname="full"),
    ]
    episodes_panel = [
        FieldPanel("episodes"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading=_("Content")),
            ObjectList(episodes_panel, heading=_("Episodes")),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )


class GenericPage(FixUrlMixin, Page):
    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")
    body_sk = RichTextField()
    body_en = RichTextField()
    body = TranslatedField("body_sk", "body_en")

    content_panels_sk = [
        FieldPanel("title", classname="full title"),
        FieldPanel("body_sk"),
    ]
    content_panels_en = [
        FieldPanel("title_en", classname="full title"),
        FieldPanel("body_en"),
    ]
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
            ObjectList(Page.promote_panels, heading="Promote"),
            ObjectList(Page.settings_panels, heading="Settings", classname="settings"),
        ]
    )


class InvitonTicketsPage(GenericPage):
    pass


class MirrorPage(RoutablePageMixin, FixUrlMixin, Page):
    title_en = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        blank=False,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )
    title_translated = TranslatedField("title", "title_en")

    mirrored_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content_panels = Page.content_panels + [
        FieldPanel("title_en", classname="full title", heading="Title EN"),
        PageChooserPanel(
            "mirrored_page",
        ),
    ]

    def serve(self, request, *args, **kwargs):
        if args[1]:
            # for subpage
            return self.mirrored_page.specific.serve(request, *args, **kwargs)
        # ignore "view" in args
        return self.mirrored_page.specific.serve(request, **kwargs)

    @route(r"^(\d+)/(.+)/")
    def subpage_with_id_in_url(self, request, object_id, slug):
        if isinstance(self.mirrored_page.specific, SpeakerIndexPage):
            speaker = Speaker.objects.get(speaker_id=object_id)
            if slug == speaker.slug:
                return speaker.serve(request)
            return redirect(speaker.get_url(request))
        elif isinstance(self.mirrored_page.specific, EventIndexPage):
            event = Event.objects.get(event_id=object_id)
            if slug == event.slug:
                return event.serve(request)
            return redirect(event.get_url(request))


def replace_tags_with_space(value):
    """Return the given HTML with spaces instead of tags."""
    return re.sub(r"</?\w+>", " ", str(value))


def ancestor_festival(page: Page):
    festival = page.get_ancestors().type(FestivalPage).first()
    if festival:
        return festival.specific
