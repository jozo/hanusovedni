from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Event


class EventAdmin(ModelAdmin):
    model = Event
    menu_icon = "date"
    # menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False
    exclude_from_explorer = (
        False  # or True to exclude pages of this type from Wagtail's explorer view
    )
    list_display = ("title", "live")
    list_filter = ("title", "live")
    search_fields = ("title",)


modeladmin_register(EventAdmin)
