import os
import textwrap
from io import BytesIO

from cairosvg import svg2png
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.dispatch import receiver
from django.utils import translation
from django.utils.formats import date_format
from PIL import Image, ImageDraw, ImageFont
from wagtail.images.models import Image as WagtailImage
from wagtail.signals import page_published

from home.models import Event
from home.models.data_models import OpenGraphImage, Speaker


def build_subtitle(event):
    date = date_format(event.date_and_time, "SHORT_DATE_FORMAT")
    speakers = ", ".join(
        f"{s.first_name} {s.last_name}"
        for s in Speaker.objects.filter(speaker_connections__event=event).only(
            "first_name", "last_name"
        )[:3]
    )
    return f"{date}  |  {speakers}"


@receiver([page_published], sender=Event)
def create_og_image_for_event(**kwargs):
    event = kwargs.get("instance")
    for lang_code, _ in settings.LANGUAGES:
        with translation.override(lang_code):
            og_file_name = "og-{}-{}-{}.png".format(
                event.slug if event else "preview", event.pk, lang_code
            )
            WagtailImage.objects.filter(title=og_file_name).delete()
            buffer = EventOGImage(
                title=event.title_translated,
                sub_title=build_subtitle(event),
                logo=event.related_festival.logo,
                title_bg_color=event.category.color if event.category else "#72c7ab",
            ).save_to_memory()
            django_image = InMemoryUploadedFile(
                buffer,
                "open_graph_image",
                og_file_name,
                "image/png",
                buffer.tell(),
                None,
            )
            wagtail_image = WagtailImage.objects.create(
                title=og_file_name, file=django_image
            )
            wagtail_image.tags.add("open-graph")
            OpenGraphImage.objects.create(
                page=event, image=wagtail_image, lang_code=lang_code
            )


class EventOGImage:
    def __init__(
        self,
        title,
        sub_title,
        logo,
        title_color=(255, 255, 255, 255),
        title_bg_color=(200, 50, 50, 255),
        sub_title_color=(255, 255, 255, 255),
        width=1200,
        height=1200,
        image_padding=100,
        text_padding=15,
        font_size=40,
        logo_width=250,
        logo_height=250,
    ):
        self.title = title
        self.sub_title = sub_title
        self.logo = logo
        self.title_color = title_color
        self.title_bg_color = title_bg_color
        self.sub_title_color = sub_title_color
        self.width = width
        self.height = height
        self.image_padding = image_padding
        self.text_padding = text_padding
        self.font_size = font_size
        self.logo_width = logo_width
        self.logo_height = logo_height

    def save(self, filename):
        image = self.generate()
        image.save(filename)

    def save_to_memory(self):
        buffer = BytesIO()
        image = self.generate()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    def generate(self):
        image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 255))
        self.draw_logo(image)
        self.draw_text(image)
        return image

    def draw_text(self, image):
        font = self.default_font(self.font_size)
        draw = ImageDraw.Draw(image)
        lines = textwrap.wrap(self.title, width=30, max_lines=3, placeholder="...")
        for i, line in enumerate(lines):
            text_width, text_height = font.getsize(line)
            text_x_start = self.image_padding
            text_y_start = (
                self.height / 2
                - 1.5 * (text_height + 2 * self.text_padding)
                + i * (text_height + 2 * self.text_padding)
            )
            rect_x_start = text_x_start - self.text_padding
            rect_y_start = text_y_start - self.text_padding
            rect_x_end = text_x_start + text_width + self.text_padding
            rect_y_end = text_y_start + text_height + self.text_padding
            draw.rectangle(
                [rect_x_start, rect_y_start, rect_x_end, rect_y_end],
                fill=self.title_bg_color,
            )
            draw.text(
                [text_x_start, text_y_start],
                line,
                self.title_color,
                font=font,
            )

        font = self.default_font(self.font_size * 2 // 3)
        draw.text(
            [text_x_start, rect_y_end + 30],
            self.sub_title,
            self.sub_title_color,
            font=font,
        )

    def default_font(self, size):
        return ImageFont.truetype(
            os.path.join(settings.PROJECT_DIR, "static/fonts/AdelleBasic_Bold.otf"),
            size,
        )

    def draw_logo(self, image):
        if self.logo:
            png_icon_str = svg2png(
                file_obj=self.logo.file,
                parent_width=self.logo_width,
                parent_height=self.logo_height,
            )
            png_icon = Image.open(BytesIO(png_icon_str))
            factor = self.logo_width / png_icon.width
            png_icon = png_icon.resize([self.logo_width, int(png_icon.height * factor)])
            image.paste(
                png_icon,
                [self.width - self.image_padding - self.logo_width, self.height // 2],
                png_icon,
            )
