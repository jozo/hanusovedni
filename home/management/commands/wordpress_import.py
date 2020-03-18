from csv import DictReader
from datetime import datetime
import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.images.models import Image

from home.models import (
    Category,
    Location,
    Speaker,
    SpeakerIndexPage,
    Event,
    EventIndexPage,
)


class Command(BaseCommand):
    help = "Imports data from Wordpress version of BHD"

    def add_arguments(self, parser):
        parser.add_argument(
            "model", type=str, choices=["categories", "locations", "events", "speakers"]
        )
        parser.add_argument("input", type=str, help="Path to input CSV file")
        parser.add_argument(
            "--img-dir", "-f", type=str, help="Path to directory with images"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        with open(options["input"], "r") as file:
            reader = DictReader(file)
            if options["model"] == "categories":
                self.import_categories(reader)
            elif options["model"] == "locations":
                self.import_locations(reader)
            elif options["model"] == "speakers":
                self.import_speakers(reader)
            elif options["model"] == "events":
                self.import_events(reader, options)

    def import_categories(self, reader):
        self.stdout.write(self.style.SUCCESS("Importing categories"))

        Category.objects.bulk_create(
            Category(title=row["category"], color=row["color"]) for row in reader
        )

        self.stdout.write(self.style.SUCCESS("Categories imported"))

    def import_locations(self, reader):
        self.stdout.write(self.style.SUCCESS("Importing locations"))

        Location.objects.bulk_create(
            Location(
                title=row["location"].strip().lower(), url_to_map="http://example.com"
            )
            for row in reader
        )

        self.stdout.write(self.style.SUCCESS("Locations imported"))

    def import_speakers(self, reader):
        self.stdout.write(self.style.SUCCESS("Importing speakers"))

        page = SpeakerIndexPage.objects.get()
        for row in reader:
            # bulk_create doesn't call save() method
            s = Speaker(
                first_name=row["first_name"] or "",
                last_name=row["last_name"],
                description=row["post_content"],
                wordpress_id=row["ID"],
            )
            page.add_child(instance=s)
            s.save_revision().publish()
            self.stdout.write(
                f"{s.pk},{s.speaker_id},{row['ID']},{s.first_name},{s.last_name}"
            )

        self.stdout.write(self.style.SUCCESS("Speakers imported"))

    def import_events(self, reader, options):
        self.stdout.write(self.style.SUCCESS("Importing events"))

        events_page = EventIndexPage.objects.get()
        for row in reader:
            # bulk_create doesn't call save() method
            try:
                if row["illustration"]:
                    illustration = Image.objects.get(title=row["illustration"])
                else:
                    illustration = None
                e = Event(
                    title=row["post_title"],
                    short_overview=row["overview"],
                    description=row["post_content"],
                    date_and_time=datetime.fromtimestamp(
                        int(row["datetime"]), pytz.timezone("Europe/Bratislava")
                    ),
                    location=(
                        Location.objects.get(title=row["location"].strip().lower())
                    ),
                    video_url=self.video_url(row["youtube_link"]),
                    # ticket_url=row["tickets_button_url"],
                    category=Category.objects.get(title=row["topic"]),
                    icon=illustration,
                    speakers=Speaker.objects.filter(
                        wordpress_id__in=row["speakers"].split(",")
                        if row["speakers"]
                        else []
                    ).all(),
                )
                events_page.add_child(instance=e)
                e.save_revision().publish()
                self.stdout.write(f"{e.pk},{e.event_id},{row['ID']},{e.title}")
            except ObjectDoesNotExist as e:
                raise

        self.stdout.write(self.style.SUCCESS("Events imported"))

    def video_url(self, from_link):
        if from_link:
            return "https://youtu.be/" + from_link.split("/")[-1]
        return ""
