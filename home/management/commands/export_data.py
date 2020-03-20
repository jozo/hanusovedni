import csv
import os

from django.core.management.base import BaseCommand
from django.db import transaction

from home.models import Category, Event, FestivalPage, Location, Speaker


class Command(BaseCommand):
    help = "Export data from Wagtail"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output-dir", "-o", type=str, help="Path to directory with output data"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Export started"))

        self.export_locations(options)
        self.export_categories(options)
        self.export_speakers(options)
        self.export_events(options)

        self.stdout.write(self.style.SUCCESS("Export finished"))

    def export_locations(self, options):
        self.stdout.write(self.style.SUCCESS("Export locations started"))
        path = os.path.join(options["output_dir"], "locations.csv")
        with open(path, "w", newline="") as file:
            writer = csv.DictWriter(file, ["id", "title", "url_to_map"])
            writer.writeheader()

            for i, location in enumerate(
                Location.objects.order_by("pk").iterator(), start=1
            ):
                writer.writerow(
                    {
                        "id": location.pk,
                        "title": location.title,
                        "url_to_map": location.url_to_map,
                    }
                )

        self.stdout.write(
            self.style.SUCCESS(f"Export locations finished - {i} locations")
        )

    def export_categories(self, options):
        self.stdout.write(self.style.SUCCESS("Export categories started"))
        path = os.path.join(options["output_dir"], "categories.csv")
        with open(path, "w", newline="") as file:
            writer = csv.DictWriter(file, ["id", "title", "color"])
            writer.writeheader()

            for i, category in enumerate(
                Category.objects.order_by("pk").iterator(), start=1
            ):
                writer.writerow(
                    {
                        "id": category.pk,
                        "title": category.title,
                        "color": category.color,
                    }
                )

        self.stdout.write(
            self.style.SUCCESS(f"Export categories finished - {i} categories")
        )

    def export_speakers(self, options):
        self.stdout.write(self.style.SUCCESS("Export speakers started"))
        path = os.path.join(options["output_dir"], "speakers.csv")
        with open(path, "w", newline="") as file:
            writer = csv.DictWriter(
                file,
                [
                    "speaker_id",
                    "title",
                    "first_name",
                    "last_name",
                    "photo",
                    "wordpress_url",
                    "description",
                ],
            )
            writer.writeheader()

            for i, speaker in enumerate(
                Speaker.objects.order_by("speaker_id").iterator(), start=1
            ):
                writer.writerow(
                    {
                        "speaker_id": speaker.speaker_id,
                        "title": speaker.title,
                        "first_name": speaker.first_name,
                        "last_name": speaker.last_name,
                        "photo": os.path.basename(speaker.photo.file.path)
                        if speaker.photo
                        else None,
                        "wordpress_url": speaker.wordpress_url,
                        "description": speaker.description,
                    }
                )

        self.stdout.write(
            self.style.SUCCESS(f"Export speakers finished - {i} speakers")
        )

    def export_events(self, options):
        self.stdout.write(self.style.SUCCESS("Export events started"))
        bhd = FestivalPage.objects.order_by("pk").all()[0]
        path = os.path.join(options["output_dir"], "events.csv")
        with open(path, "w", newline="") as file:
            writer = csv.DictWriter(
                file,
                [
                    "event_id",
                    "title",
                    "category",
                    "date_and_time",
                    "location",
                    "video_url",
                    "ticket_url",
                    "show_on_festivalpage",
                    "icon",
                    "related_festival",
                    "speakers",
                    "wordpress_url",
                    "short_overview",
                    "description",
                ],
            )
            writer.writeheader()

            for i, event in enumerate(
                Event.objects.order_by("event_id").iterator(), start=1
            ):
                writer.writerow(
                    {
                        "event_id": event.event_id,
                        "title": event.title,
                        "category": event.category.title,
                        "date_and_time": event.date_and_time.isoformat(),
                        "location": event.location.title,
                        "video_url": event.video_url,
                        "ticket_url": event.ticket_url,
                        "show_on_festivalpage": event.show_on_festivalpage,
                        "icon": event.icon.title + ".png" if event.icon else None,
                        "related_festival": "bhd"
                        if event.related_festival == bhd
                        else "khd",
                        "speakers": ",".join(
                            str(s.speaker_id) for s in event.speakers.all()
                        ),
                        "wordpress_url": event.wordpress_url,
                        "short_overview": event.short_overview,
                        "description": event.description,
                    }
                )

        self.stdout.write(self.style.SUCCESS(f"Export events finished - {i} events"))
