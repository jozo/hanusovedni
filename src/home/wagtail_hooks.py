from django.contrib import admin
from django.contrib.auth.models import Permission
from django.db import models
from django.db.models import Q
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import gettext as _
from wagtail import hooks
from wagtail.admin import messages
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .fields import TranslatedField
from .models import Event, Speaker
from .signals.cache import CloudFlare


class YearFilter(admin.SimpleListFilter):
    title = _("year")
    parameter_name = "year"

    def lookups(self, request, model_admin):
        return [(year, year) for year in range(timezone.now().year, 2012, -1)]

    def queryset(self, request, queryset):
        if self.value():
            if queryset.model == Event:
                return queryset.filter(date_and_time__year=self.value())
            elif queryset.model == Speaker:
                return queryset.filter(
                    Q(speaker_connections__event__date_and_time__year=self.value())
                    | Q(host_connections__event__date_and_time__year=self.value())
                ).distinct()


class EventAdmin(ModelAdmin):
    model = Event
    menu_icon = "date"
    add_to_settings_menu = False
    exclude_from_explorer = (
        False  # or True to exclude pages of this type from Wagtail's explorer view
    )
    list_display = ["title", "latest_revision_created_at", "live"]
    ordering = ["-latest_revision_created_at"]
    list_filter = [YearFilter, "live", "category"]
    search_fields = ["title"]
    list_per_page = 15


class SpeakerAdmin(ModelAdmin):
    model = Speaker
    menu_icon = "user"
    add_to_settings_menu = False
    exclude_from_explorer = (
        False  # or True to exclude pages of this type from Wagtail's explorer view
    )
    list_display = ["first_name", "last_name", "latest_revision_created_at", "live"]
    ordering = ["-latest_revision_created_at"]
    list_filter = [YearFilter, "live"]
    search_fields = ["title"]
    list_per_page = 15


modeladmin_register(EventAdmin)
modeladmin_register(SpeakerAdmin)


@register_setting
class TranslationSettings(BaseSiteSetting):
    watch_video_button_sk = models.TextField(blank=True)
    watch_video_button_en = models.TextField(blank=True)
    watch_video_button = TranslatedField(
        "watch_video_button_sk", "watch_video_button_en"
    )

    buy_ticket_button_sk = models.TextField(blank=True)
    buy_ticket_button_en = models.TextField(blank=True)
    buy_ticket_button = TranslatedField("buy_ticket_button_sk", "buy_ticket_button_en")

    buy_ticket2_button_sk = models.TextField(blank=True)
    buy_ticket2_button_en = models.TextField(blank=True)
    buy_ticket2_button = TranslatedField(
        "buy_ticket2_button_sk", "buy_ticket2_button_en"
    )

    # Permanentka
    season_ticket_button_sk = models.TextField(blank=True)
    season_ticket_button_en = models.TextField(blank=True)
    season_ticket_button = TranslatedField(
        "season_ticket_button_sk", "season_ticket_button_en"
    )

    season_ticket_url = models.URLField(blank=True)

    content_panels_sk = [
        FieldPanel("watch_video_button_sk"),
        FieldPanel("buy_ticket_button_sk"),
        FieldPanel("buy_ticket2_button_sk"),
        FieldPanel("season_ticket_button_sk"),
        FieldPanel("season_ticket_url"),
    ]
    content_panels_en = [
        FieldPanel("watch_video_button_en"),
        FieldPanel("buy_ticket_button_en"),
        FieldPanel("buy_ticket2_button_en"),
        FieldPanel("season_ticket_button_en"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
        ]
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
        CloudFlare().purge_everything()


@hooks.register("register_permissions")
def register_permissions():
    """We register these permissions so we can limit which groups can delete speakers/events"""
    return Permission.objects.filter(
        content_type__app_label="home",
        codename__in=[
            "add_speaker",
            "change_speaker",
            "delete_speaker",
            "add_event",
            "change_event",
            "delete_event",
        ],
    )


@hooks.register("before_delete_page")
def disable_delete(request, page):
    """Disable deleting of speakers/events

    We don't want it because it breaks urls and connections between speakers and events.
    We disable it only during POST request (so in the final stage of deleting). This means
    delete confirmation page is displayed. From there user can alternatively unpublish the page.
    """
    if (
        request.user.username != "admin"
        and page.specific_class in [Speaker, Event]
        and request.method == "POST"
    ):
        messages.warning(
            request,
            _("Page '{0}' can not be deleted. You can only unpublish it.").format(
                page.get_admin_display_title()
            ),
        )
        return redirect("wagtailadmin_pages:delete", page.pk)
