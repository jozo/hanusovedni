from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext as _
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Event, Speaker


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
    ordering = ["latest_revision_created_at"]
    list_filter = [YearFilter, "live"]
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
    ordering = ["latest_revision_created_at"]
    list_filter = [YearFilter, "live"]
    search_fields = ["title"]
    list_per_page = 15


modeladmin_register(EventAdmin)
modeladmin_register(SpeakerAdmin)
