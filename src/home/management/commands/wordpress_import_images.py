import os
from csv import DictReader

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.images.models import Image
from wagtail.search import index as search_index

from home.models import Speaker


class Command(BaseCommand):
    help = "Imports images from Wordpress version of BHD"

    def add_arguments(self, parser):
        parser.add_argument(
            "--speakers_csv", "-s", type=str, help="Path to speakers CSV file"
        )
        parser.add_argument(
            "--from_dir", "-f", type=str, help="Path to directory with images"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Importing images"))

        with open(options["speakers_csv"], "r") as file:
            for row in DictReader(file):
                if not row["filename"]:
                    self.stdout.write(
                        self.style.WARNING(
                            f"====> skipping {row['post_name']}, {row['post_title']}"
                        )
                    )
                    continue
                image_path = os.path.join(options["from_dir"], row["filename"])
                with open(image_path, "rb") as image_file:
                    image = Image(title=row["post_title"])
                    if row["filename"].lower().endswith(".jpg") or row[
                        "filename"
                    ].lower().endswith(".jpeg"):
                        image_filename = f"{row['first_name']} {row['last_name']}.jpg"
                    elif row["filename"].lower().endswith(".png"):
                        image_filename = f"{row['first_name']} {row['last_name']}.png"
                    else:
                        raise ValueError("Unknown file format")
                    image.file = ImageFile(file=image_file, name=image_filename)
                    image.file_size = image.file.size

                    image.file.seek(0)
                    image._set_file_hash(image.file.read())
                    image.file.seek(0)

                    # Reindex the image to make sure all tags are indexed
                    search_index.insert_or_update_object(image)
                    image.save()
                    image.tags.add("speaker")

                    speaker = Speaker.objects.get(wordpress_id=row["ID"])
                    speaker.photo = image
                    speaker.save()

                    self.stdout.write(self.style.SUCCESS(f"{image.pk},{image.title}"))

        self.stdout.write(self.style.SUCCESS("Importing images finished"))
