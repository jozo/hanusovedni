from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Event, Speaker


class EventAdmin(ModelAdmin):
    model = Event
    menu_icon = "date"
    add_to_settings_menu = False
    exclude_from_explorer = (
        False  # or True to exclude pages of this type from Wagtail's explorer view
    )
    list_display = ["title", "live"]
    list_filter = ["live"]
    search_fields = ["title"]
    list_per_page = 15


class SpeakerAdmin(ModelAdmin):
    model = Speaker
    menu_icon = "user"
    add_to_settings_menu = False
    exclude_from_explorer = (
        False  # or True to exclude pages of this type from Wagtail's explorer view
    )
    list_display = ["first_name", "last_name", "live"]
    list_filter = ["live"]
    search_fields = ["title"]
    list_per_page = 15


modeladmin_register(EventAdmin)
modeladmin_register(SpeakerAdmin)
