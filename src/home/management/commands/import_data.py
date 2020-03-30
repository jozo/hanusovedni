import csv
import os
from datetime import datetime
from glob import glob

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.images.models import Image
from wagtail.search import index as search_index

from home.models import (
    Category,
    Event,
    EventIndexPage,
    FestivalPage,
    Location,
    Speaker,
    SpeakerIndexPage,
)


class Command(BaseCommand):
    """
    Pages which must be created before:
    * BHD festival
    * KHD festival
    * SpeakerIndexPage
    * EventIndexPage
    """

    help = "Import data to Wagtail"

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv-dir", "-c", type=str, help="Path to directory with CSV files"
        )
        parser.add_argument(
            "--images-dir", "-i", type=str, help="Path to directory with images"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Import started"))

        self.import_illustrations(options)
        self.import_locations(options)
        self.import_categories(options)
        self.import_speakers(options)
        self.import_events(options)

        self.stdout.write(self.style.SUCCESS("Import finished"))

    def import_illustrations(self, options):
        self.stdout.write(self.style.SUCCESS("Import illustrations started"))

        pattern = os.path.join(options["images_dir"], "illustration*.png")

        for i, filepath in enumerate(sorted(glob(pattern)), start=1):
            with open(filepath, "rb") as image_file:
                basename = os.path.basename(filepath)
                name = os.path.splitext(basename)[0]
                self.create_image(
                    image_file, title=name, filename=name + ".png", tag="illustration"
                )

        self.stdout.write(
            self.style.SUCCESS(f"Import illustrations finished - {i} locations")
        )

    def create_image(self, image_file, title, filename, tag):
        image = Image(title=title)
        image.file = ImageFile(file=image_file, name=filename)
        image.file_size = image.file.size
        image.file.seek(0)
        image._set_file_hash(image.file.read())
        image.file.seek(0)
        # Reindex the image to make sure all tags are indexed
        search_index.insert_or_update_object(image)
        image.save()
        image.tags.add(tag)
        return image

    def import_locations(self, options):
        self.stdout.write(self.style.SUCCESS("Import locations started"))

        path = os.path.join(options["csv_dir"], "locations.csv")
        with open(path, "r", newline="") as file:
            reader = csv.DictReader(file)

            for i, row in enumerate(reader, start=1):
                Location.objects.create(
                    title=row["title"], url_to_map=row["url_to_map"]
                )

        self.stdout.write(
            self.style.SUCCESS(f"Import locations finished - {i} locations")
        )

    def import_categories(self, options):
        self.stdout.write(self.style.SUCCESS("Import categories started"))

        path = os.path.join(options["csv_dir"], "categories.csv")
        with open(path, "r", newline="") as file:
            reader = csv.DictReader(file)

            for i, row in enumerate(reader, start=1):
                Category.objects.create(title=row["title"], color=row["color"])

        self.stdout.write(
            self.style.SUCCESS(f"Import categories finished - {i} categories")
        )

    def import_speakers(self, options):
        self.stdout.write(self.style.SUCCESS("Import speakers started"))

        parent = SpeakerIndexPage.objects.get()
        path = os.path.join(options["csv_dir"], "speakers.csv")

        with open(path, "r", newline="") as file:
            reader = csv.DictReader(file)

            for i, row in enumerate(reader, start=1):
                parent.add_child(
                    instance=Speaker(
                        speaker_id=row["speaker_id"],
                        title=row["title"],
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                        wordpress_url=row["wordpress_url"],
                        description=row["description"],
                        photo=self.create_speaker_photo(row, options),
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f"Import speakers finished - {i} speakers")
        )

    def create_speaker_photo(self, row, options):
        if not row["photo"]:
            return None

        path = os.path.join(options["images_dir"], row["photo"])
        with open(path, "rb") as file:
            return self.create_image(
                image_file=file,
                title=row["title"],
                filename=row["photo"],
                tag="speaker",
            )

    def import_events(self, options):
        self.stdout.write(self.style.SUCCESS("Import events started"))

        bhd = FestivalPage.objects.order_by("pk").all()[0]
        khd = FestivalPage.objects.order_by("pk").all()[1]
        parent = EventIndexPage.objects.get()

        path = os.path.join(options["csv_dir"], "events.csv")
        with open(path, "r", newline="") as file:
            reader = csv.DictReader(file)

            for i, row in enumerate(reader, start=1):
                parent.add_child(
                    instance=Event(
                        event_id=row["event_id"],
                        title=row["title"],
                        category=Category.objects.get(title=row["category"]),
                        date_and_time=datetime.fromisoformat(row["date_and_time"]),
                        location=Location.objects.get(title=row["location"]),
                        video_url=row["video_url"],
                        ticket_url=row["ticket_url"],
                        show_on_festivalpage=row["show_on_festivalpage"],
                        icon=self.icon(row["icon"]),
                        related_festival=bhd
                        if row["related_festival"] == "bhd"
                        else khd,
                        speakers=Speaker.objects.filter(
                            speaker_id__in=row["speakers"].split(",")
                            if row["speakers"]
                            else []
                        ),
                        wordpress_url=row["wordpress_url"],
                        short_overview=row["short_overview"],
                        description=row["description"],
                    )
                )

        self.stdout.write(self.style.SUCCESS(f"Import events finished - {i} events"))

    def icon(self, filename):
        if not filename:
            return None

        return Image.objects.get(title=filename.split(".")[0])
