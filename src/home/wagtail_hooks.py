from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from wagtail.admin.edit_handlers import FieldPanel, ObjectList, TabbedInterface
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting

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
                return queryset.filter(events__date_and_time__year=self.value()).distinct()


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
class TranslationSettings(BaseSetting):
    watch_video_button_sk = models.TextField(blank=True)
    watch_video_button_en = models.TextField(blank=True)
    watch_video_button = TranslatedField(
        "watch_video_button_sk", "watch_video_button_en"
    )

    buy_ticket_button_sk = models.TextField(blank=True)
    buy_ticket_button_en = models.TextField(blank=True)
    buy_ticket_button = TranslatedField("buy_ticket_button_sk", "buy_ticket_button_en")

    content_panels_sk = [
        FieldPanel("watch_video_button_sk"),
        FieldPanel("buy_ticket_button_sk"),
    ]
    content_panels_en = [
        FieldPanel("watch_video_button_en"),
        FieldPanel("buy_ticket_button_en"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels_sk, heading="Content SK"),
            ObjectList(content_panels_en, heading="Content EN"),
        ]
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        CloudFlare().purge_everything()
